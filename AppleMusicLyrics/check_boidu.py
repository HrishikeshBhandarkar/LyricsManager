import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://artwork.boidu.dev/"


def check(song, artist, album="", duration=None, timeout=15):
    params = {"s": song, "a": artist}
    if album:
        params["al"] = album
    if duration:
        params["d"] = str(int(duration))
    url = API + "?" + urllib.parse.urlencode(params)
    print("GET", url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", "replace")
        data = json.loads(body)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    static = data.get("static")
    animated = data.get("animated")
    video = data.get("videoUrl")
    print("=" * 50)
    if not data.get("albumId"):
        print("RESULT: NOT FOUND (no albumId) - nothing to use")
    elif video:
        print("RESULT: ANIMATED VIDEO available (mp4) -> will animate in app")
    elif animated:
        print("RESULT: ANIMATED available (HLS m3u8) -> animates with hls.js / Safari")
    elif static:
        print("RESULT: STATIC ONLY -> app uses this as normal art")
    else:
        print("RESULT: nothing usable")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Check if artwork.boidu.dev returns art for a song")
    p.add_argument("song", help="song title")
    p.add_argument("--artist", "-a", default="", help="artist name (optional)")
    p.add_argument("--album", "-al", default="", help="album name (optional, improves match)")
    p.add_argument("--duration", "-d", type=float, help="song duration in seconds (optional)")
    p.add_argument("--timeout", type=int, default=15)
    args = p.parse_args()
    try:
        check(args.song, args.artist, args.album, args.duration, args.timeout)
    except Exception as e:
        print("ERROR:", type(e).__name__, e, file=sys.stderr)
        sys.exit(1)
