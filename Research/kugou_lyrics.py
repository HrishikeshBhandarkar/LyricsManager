"""
KuGou word-by-word (KRC) lyrics fetcher.

Based on the actual working implementation from kangkang520/kugou-lyric
(github.com/kangkang520/kugou-lyric) — an unauthenticated, unsigned flow:

  1. Search lyrics.kugou.com/search?keyword=...&duration=...  (ms)
  2. Download lyrics.kugou.com/download?id=...&accesskey=...&fmt=krc
  3. Base64-decode the response's `content` field
  4. Decrypt: skip first 4 bytes, XOR remaining bytes with a fixed 16-byte
     key cyclically, then zlib-inflate
  5. Parse the resulting KRC markup (similar bracket structure to QQ's QRC)

No DES, no request signing, no VPN-gated client API — this is why KuGou is
a more practical target than QQ Music for word-by-word lyrics.

Requires: pip install requests
"""

import requests
import base64
import zlib
import re
import sys

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

SEARCH_URL = "http://lyrics.kugou.com/search"
DOWNLOAD_URL = "http://lyrics.kugou.com/download"

# Fixed KRC decryption key (16 bytes), sourced from kangkang520/kugou-lyric.
KRC_ENCODE_KEY = bytes([64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105])


def decode_krc(content: bytes) -> str:
    """Strip 4-byte magic header, XOR-decrypt, zlib-inflate."""
    payload = content[4:]
    decrypted = bytes(b ^ KRC_ENCODE_KEY[i % 16] for i, b in enumerate(payload))
    return zlib.decompress(decrypted).decode("utf-8", errors="ignore")


def search_lyrics(name: str, duration_ms: int):
    """Search KuGou for lyric candidates matching a song name + duration."""
    resp = requests.get(
        SEARCH_URL,
        params={"ver": 1, "man": "yes", "client": "pc", "keyword": name, "duration": duration_ms},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"No lyric candidates found for '{name}' ({duration_ms}ms)")
    return candidates


def fetch_krc(lyric_id: str, accesskey: str) -> str:
    resp = requests.get(
        DOWNLOAD_URL,
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


def parse_krc(krc_text: str):
    """Parse decrypted KRC markup into lines of (word, start_ms, dur_ms).
    KRC line format: [line_start,line_dur]<word_start,word_dur,0>word<...>word...
    """
    lines_out = []
    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*)")
    word_pattern = re.compile(r"<(\d+),(\d+),\d+>([^<]*)")

    for raw_line in krc_text.splitlines():
        m = line_pattern.match(raw_line.strip())
        if not m:
            continue
        words = word_pattern.findall(m.group(3))
        if words:
            lines_out.append(
                [(text.strip(), int(start), int(dur)) for start, dur, text in words if text.strip()]
            )
    return lines_out


def main():
    if len(sys.argv) < 3:
        print("Usage: python kugou_lyrics.py \"<song name>\" <duration_seconds>")
        print("Example: python kugou_lyrics.py \"linkin park - numb\" 187")
        sys.exit(1)

    name = sys.argv[1]
    duration_ms = int(float(sys.argv[2]) * 1000)

    print(f"Searching KuGou for: {name} ({duration_ms}ms)\n")

    try:
        candidates = search_lyrics(name, duration_ms)
    except Exception as e:
        print(f"Search failed: {e}")
        sys.exit(1)

    for i, c in enumerate(candidates[:5]):
        print(f"  [{i}] id={c.get('id')} accesskey={c.get('accesskey')} krctype={c.get('krctype')}")

    choice = 0
    if len(candidates) > 1:
        try:
            choice = int(input("\nPick a result number [0]: ") or 0)
        except ValueError:
            choice = 0

    picked = candidates[choice]
    print(f"\nFetching KRC for id={picked['id']} ...")

    try:
        krc_text = fetch_krc(picked["id"], picked["accesskey"])
    except Exception as e:
        print(f"Fetch/decrypt failed: {e}")
        sys.exit(1)

    parsed = parse_krc(krc_text)

    if not parsed:
        print("\nCouldn't parse word-by-word structure — printing raw decrypted KRC instead:\n")
        print(krc_text[:2000])
        return

    print(f"\nParsed {len(parsed)} lines of word-by-word lyrics.\n")
    for line in parsed[:5]:
        line_str = " ".join(f"{w}[{start}]" for w, start, dur in line)
        print(line_str)
    print("\n(showing first 5 lines only)")


if __name__ == "__main__":
    main()
