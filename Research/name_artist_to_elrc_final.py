"""
Song name + artist -> KuGou word-by-word lyrics -> eLRC (Apple-Music-style
enhanced LRC with voice tags [v1]/[v2] and background-vocal [bg] tags).

Pipeline:
  1. iTunes Search API (itunes.apple.com/search) to resolve the song and
     read its duration automatically — you don't need to know/enter it.
     This replaces KuGou's own general song search, which is unreliable;
     iTunes' catalog search is public, unauthenticated, and stable.
  2. Lyric search (lyrics.kugou.com/search) using that duration to find the
     best-matching KRC candidate.
  3. Download + decrypt the KRC blob (XOR + zlib, see kugou_lyrics.py).
  4. Convert KRC's word-timing markup into eLRC:
       - one [mm:ss.xx] line-start tag per line
       - a voice tag: [v1] by default, [v2] if the line looks like a
         second voice/duet part (heuristic: alternating-line detection is
         NOT reliable from KRC alone, so this defaults everything to v1
         unless you pass --alternate to force v1/v2 alternation)
       - a [bg] tag for lines that were originally wrapped in parentheses
         in the source lyric (KuGou/QQ/Apple convention for background
         vocals), with the parentheses stripped from the visible text
       - per-word start times as {mm:ss.xx} immediately before each word

  eLRC line examples this produces (absolute per-word timestamps, angle
  brackets, first word matching the line's own start time):
    [00:12.340][v1]Word<00:12.340>by<00:12.610>word<00:12.820>
    [00:45.100][bg]Ooh<00:45.100>ooh<00:45.400>

  NOTE: there is no single universal "eLRC" standard — different apps
  (Apple Music, Musixmatch exporters, various community tools) use
  slightly different bracket conventions. This follows the
  voice-tag + per-word-curly-timestamp convention that's common across
  those community eLRC tools. If your existing eLRC generator/parser
  expects a different bracket style, tell me the exact format it reads
  and I'll adjust the output function — that's a one-function change.

Requires: pip install requests
"""

SCRIPT_VERSION = "v4-absolute-word-timestamps"


import requests
import base64
import zlib
import re
import sys
import argparse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
LYRIC_SEARCH_URL = "http://lyrics.kugou.com/search"
LYRIC_DOWNLOAD_URL = "http://lyrics.kugou.com/download"

KRC_ENCODE_KEY = bytes([64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105])


# ---------- iTunes lookup (song resolution + duration) ----------

def find_song(name: str, artist: str):
    """iTunes Search API — public, unauthenticated, stable. Returns a dict
    with at least: trackName, artistName, trackTimeMillis."""
    resp = requests.get(
        ITUNES_SEARCH_URL,
        params={"term": f"{name} {artist}", "entity": "song", "limit": 10},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        raise RuntimeError(f"No songs found on iTunes for '{name}' by '{artist}'")

    # Prefer a result whose artist roughly matches what was asked for.
    artist_lower = artist.lower()
    for track in results:
        if artist_lower in track.get("artistName", "").lower():
            return track
    return results[0]  # fallback: top result


def search_lyric_candidates(name: str, artist: str, duration_ms: int):
    """Tries a few keyword/duration combinations before giving up, since
    KuGou's lyric search is strict about duration matching and iTunes'
    duration (radio edit, clean version, etc.) doesn't always line up
    closely with KuGou's stored version."""
    attempts = [
        {"keyword": f"{name} - {artist}", "duration": duration_ms},
        {"keyword": f"{artist} - {name}", "duration": duration_ms},
        {"keyword": f"{name} {artist}", "duration": duration_ms},
        {"keyword": f"{name} - {artist}", "duration": 0},  # no duration filter
    ]

    last_response = None
    for attempt in attempts:
        print(f"  trying keyword='{attempt['keyword']}' duration={attempt['duration']}", file=sys.stderr)
        resp = requests.get(
            LYRIC_SEARCH_URL,
            params={"ver": 1, "man": "yes", "client": "pc", **attempt},
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        last_response = data
        candidates = data.get("candidates", [])
        if candidates:
            print(f"  -> matched", file=sys.stderr)
            return candidates

    raise RuntimeError(f"No lyric candidates found after {len(attempts)} attempts. Last response: {last_response}")


def decode_krc(content: bytes) -> str:
    payload = content[4:]
    decrypted = bytes(b ^ KRC_ENCODE_KEY[i % 16] for i, b in enumerate(payload))
    return zlib.decompress(decrypted).decode("utf-8", errors="ignore")


def fetch_krc(lyric_id: str, accesskey: str) -> str:
    resp = requests.get(
        LYRIC_DOWNLOAD_URL,
        params={"ver": 1, "client": "pc", "id": lyric_id, "accesskey": accesskey, "fmt": "krc", "charset": "utf8"},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("fmt") != "krc" or not data.get("content"):
        raise RuntimeError(f"Unexpected download response: {data}")
    raw = base64.b64decode(data["content"])
    return decode_krc(raw)


# ---------- KRC parsing ----------

LINE_RE = re.compile(r"\[(\d+),(\d+)\](.*)")
WORD_RE = re.compile(r"<(\d+),(\d+),\d+>([^<]*)")


def parse_krc(krc_text: str):
    """Returns list of lines: {start_ms, words: [(text, start_ms, dur_ms)]}"""
    lines_out = []
    for raw_line in krc_text.splitlines():
        m = LINE_RE.match(raw_line.strip())
        if not m:
            continue
        line_start = int(m.group(1))
        words = WORD_RE.findall(m.group(3))
        parsed_words = [(text, int(start), int(dur)) for start, dur, text in words if text.strip()]
        if parsed_words:
            lines_out.append({"start_ms": line_start, "words": parsed_words})
    return lines_out


# ---------- eLRC conversion ----------

def ms_to_tag(ms: int) -> str:
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds - minutes * 60
    return f"{minutes:02d}:{seconds:05.2f}"


def is_background_line(words) -> bool:
    """Heuristic: KuGou/QQ/Apple convention wraps background-vocal lines in
    parentheses in the original lyric text."""
    joined = "".join(w[0] for w in words).strip()
    return joined.startswith("(") or joined.startswith("（")


def strip_parens(text: str) -> str:
    return text.strip("()（） ")


def to_elrc(parsed_lines, alternate_voices: bool = False) -> str:
    out_lines = []
    voice_toggle = 1

    for line in parsed_lines:
        words = line["words"]
        bg = is_background_line(words)

        voice_tag = f"v{voice_toggle}" if alternate_voices else "v1"
        if alternate_voices:
            voice_toggle = 2 if voice_toggle == 1 else 1

        tags = f"[{voice_tag}]"
        if bg:
            tags = "[bg]" + tags

        line_start_tag = f"[{ms_to_tag(line['start_ms'])}]"

        word_parts = []
        for text, word_start_ms, _dur_ms in words:
            clean_text = strip_parens(text) if bg else text
            if not clean_text.strip():
                continue
            absolute_ms = line["start_ms"] + word_start_ms
            word_parts.append(f"{clean_text}<{ms_to_tag(absolute_ms)}>")

        out_lines.append(line_start_tag + tags + "".join(word_parts))

    return "\n".join(out_lines)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="song name")
    ap.add_argument("artist", help="artist name")
    ap.add_argument("--alternate", action="store_true", help="alternate v1/v2 tags per line (duet heuristic)")
    ap.add_argument("-o", "--output", help="output .elrc file path (default: prints to stdout)")
    args = ap.parse_args()

    print(f"[{SCRIPT_VERSION}]", file=sys.stderr)

    print(f"Looking up '{args.name}' by '{args.artist}' ...", file=sys.stderr)
    try:
        song = find_song(args.name, args.artist)
        duration_ms = int(song["trackTimeMillis"])
        resolved_name = song.get("trackName", args.name)
        resolved_artist = song.get("artistName", args.artist)
        print(f"Found: {resolved_name} - {resolved_artist} "
              f"({duration_ms/1000:.0f}s)", file=sys.stderr)

        candidates = search_lyric_candidates(resolved_name, resolved_artist, duration_ms)
        picked = candidates[0]
        print(f"Using lyric candidate id={picked['id']}", file=sys.stderr)

        krc_text = fetch_krc(picked["id"], picked["accesskey"])
        parsed = parse_krc(krc_text)
        if not parsed:
            raise RuntimeError("KRC decrypted but no word-by-word lines could be parsed")

        elrc = to_elrc(parsed, alternate_voices=args.alternate)
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(elrc)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(elrc)


if __name__ == "__main__":
    main()
