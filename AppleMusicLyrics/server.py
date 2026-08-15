#!/usr/bin/env python3
"""
server.py — Self-hosted artwork + static server for the Apple Music lyrics player.

Instead of relying on third-party artwork proxies (artwork.boidu.dev), this server
fetches artwork DIRECTLY from Apple on your own:

  STILL artwork  ->  public iTunes Search API (no auth) + CDN size-upgrade
  ANIMATED art   ->  Apple Music album/song web page. The moving cover is embedded
                     in the public page as "videoArtwork.dictionary.motionDetailSquare.video"
                     (an HLS .m3u8 stream). The browser streams it with hls.js directly
                     from Apple's media CDN — no ffmpeg, no token.

Serves the app itself too, so just open http://localhost:8765/ in your browser.

USAGE
    python server.py                 # serve on http://localhost:8765
    python server.py --port 8000
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from functools import lru_cache
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

API_PORT = 8765
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def http_get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def itunes_search(term, country="us", limit=5):
    url = (
        "https://itunes.apple.com/search?term=" + urllib.parse.quote(term) +
        "&entity=song&country=" + country + "&limit=" + str(limit)
    )
    return json.loads(http_get(url)).get("results", [])


def upscale_static_url(url, size=1200):
    if url and "100x100bb" in url:
        return re.sub(r"/100x100bb", "/%dx%dbb" % (size, size), url)
    return url


def page_motion_artwork(html):
    """Pull HLS motion-cover URLs out of an Apple Music album/song page."""
    found = {}
    for variant in ("motionDetailSquare", "motionSquare", "motionDetailTall", "motionTall"):
        idx = html.find('"%s"' % variant)
        if idx < 0:
            continue
        seg = html[idx:idx + 8000]
        m = re.search(r'"video":"(https:[^"\\]+?\.m3u8[^"\\]*)"', seg)
        if m:
            found[variant] = m.group(1)
    return found


def scrape_motion(urls):
    for url in urls:
        if not url:
            continue
        try:
            html = http_get(url).decode("utf-8", "ignore")
            motions = page_motion_artwork(html)
            if motions:
                return motions
        except Exception:
            continue
    return {}


def pick_best_variant(master_url, prefer_avc=True):
    """Fetch an HLS master, pick the highest-resolution variant.
    Returns (variant_hls_url, direct_mp4_url, codecs) or (None, None, None)."""
    try:
        body = http_get(master_url).decode("utf-8", "ignore")
    except Exception:
        return None, None, None
    base = master_url.rsplit("/", 1)[0] + "/"
    best = None
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#EXT-X-STREAM-INF:") and i + 1 < len(lines):
            u2 = lines[i + 1].strip()
            if not u2.startswith("#") and u2:
                m = re.search(r"RESOLUTION=(\d+)x(\d+)", ln)
                w = int(m.group(1)) if m else 0
                codecs = re.search(r'CODECS="([^"]+)"', ln)
                codec = codecs.group(1) if codecs else ""
                variant = u2 if u2.startswith("http") else base + u2
                if best is None or w > best[0]:
                    best = (w, variant, codec)
            i += 1
        i += 1
    if not best:
        return None, None, None
    variant, codec = best[1], best[2]
    mp4 = variant.rsplit(".m3u8", 1)[0] + "-.mp4"
    return variant, mp4, codec


@lru_cache(maxsize=256)
def resolve(song, artist="", country="us"):
    if not song:
        raise ValueError("missing song")

    t = song.strip()
    a = artist.strip()
    clean_t = re.sub(r"[\(\[]([^\)\]]*)[\)\]]", r"\1", t)
    queries = []
    for q in ("%s %s" % (a, clean_t), "%s %s" % (clean_t, a), clean_t, t):
        q = q.strip()
        if q and q not in queries:
            queries.append(q)

    hits = []
    seen = set()
    for q in queries:
        try:
            for r in itunes_search(q, country):
                if r.get("trackId") in seen:
                    continue
                seen.add(r.get("trackId"))
                hits.append(r)
        except Exception:
            continue
        if hits:
            break

    if not hits:
        return {"found": False, "reason": "no iTunes match"}

    hit = hits[0]
    if a:
        for r in hits:
            if (r.get("artistName") or "").lower() == a.lower():
                hit = r
                break

    static = upscale_static_url(hit.get("artworkUrl100"))
    album_url = hit.get("collectionViewUrl")
    song_url = hit.get("trackViewUrl")

    motions = scrape_motion([album_url, song_url])
    master = motions.get("motionDetailSquare") or motions.get("motionSquare")
    variant_hls, direct_mp4, _codec = pick_best_variant(master) if master else (None, None, None)

    return {
        "found": True,
        "name": hit.get("trackName") or hit.get("collectionName"),
        "artist": hit.get("artistName") or "",
        "albumId": hit.get("collectionId"),
        "static": static,
        "albumUrl": album_url,
        "videoUrl": direct_mp4,
        "videoUrlHls": master,
        "videoUrlTall": motions.get("motionDetailTall") or motions.get("motionTall") or None,
    }


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        if path == "/api/art":
            self._api_art()
            return
        super().do_GET()

    def _api_art(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        song = (qs.get("song") or qs.get("s") or [""])[0]
        artist = (qs.get("artist") or qs.get("a") or [""])[0]
        country = (qs.get("country") or ["us"])[0]
        try:
            data = resolve(song, artist, country)
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
        except Exception as e:
            body = json.dumps({"found": False, "reason": str(e)}, ensure_ascii=False).encode("utf-8")
            self.send_response(502)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stdout.write("[%s] %s\n" % (self.address_string()[:0] or "server", fmt % args))


def main():
    p = argparse.ArgumentParser(description="Self-hosted artwork proxy + static server")
    p.add_argument("--port", type=int, default=API_PORT, help="port (default 8765)")
    p.add_argument("--directory", default=".", help="directory to serve (default: this script's dir)")
    args = p.parse_args()

    here = __import__("os").path.abspath(args.directory)
    handler = lambda *a, **k: Handler(*a, directory=here, **k)
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print("Lyrics player running at  http://localhost:%d/" % args.port)
    print("Artwork API:             http://localhost:%d/api/art?song=...&artist=..." % args.port)
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
