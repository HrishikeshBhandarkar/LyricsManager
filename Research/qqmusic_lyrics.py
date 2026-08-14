"""
QQ Music word-by-word (QRC) lyrics fetcher.

Pipeline:
  1. Search for a song by keyword -> get its songmid
  2. Request lyric data (QRC = word-by-word, if available; falls back to plain LRC)
  3. Decrypt the QRC blob (triple-DES-EDE x3, then zlib inflate)
  4. Parse the QRC XML-ish markup into (start_ms, duration_ms, word) tuples

NOTE ON RELIABILITY:
  This uses QQ Music's unofficial, undocumented `musicu.fcg` endpoint and a
  reverse-engineered decryption scheme (DES keys below, sourced from public
  open-source decoders such as xmcp/QRCD and WXRIW/QQMusicDecoder). Tencent
  can change request signing / response shape at any time, which will break
  this. Treat it as "works today, verify before relying on it" rather than
  a stable, documented API.

Requires: pip install requests pycryptodome
"""

import requests
import zlib
import re
import sys
import json
from Crypto.Cipher import DES3

HEADERS = {
    "Referer": "https://y.qq.com/",
    "Origin": "https://y.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

SEARCH_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg"
LYRIC_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg"

# Reverse-engineered QRC decryption keys (triple-DES, EDE mode, 3 rounds).
# Source: public decoders (xmcp/QRCD lib_qrc_decoder.cpp; WXRIW/QQMusicDecoder).
_KEY1 = b"!@#)(NHLiuy*$%^&"
_KEY2 = b"123ZXC!@#)(*$%^&"
_KEY3 = b"!@#)(*$%^&abcDEF"


def _des3_decrypt(data: bytes, key: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.decrypt(data)


def _des3_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.encrypt(data)


def decrypt_qrc(hex_str: str) -> str:
    """Decrypt a hex-encoded encrypted QRC blob into raw XML text."""
    raw = bytes.fromhex(hex_str.strip())
    # pad to multiple of 8 for DES block size safety (should already be aligned)
    pad_len = (-len(raw)) % 8
    if pad_len:
        raw += b"\x00" * pad_len

    step1 = _des3_decrypt(raw, _KEY1)
    step2 = _des3_encrypt(step1, _KEY2)
    step3 = _des3_decrypt(step2, _KEY3)

    return zlib.decompress(step3).decode("utf-8", errors="ignore")


def search_song(keyword: str, count: int = 5):
    """Search QQ Music for a song, return list of {songmid, name, singer}."""
    payload = {
        "req": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "num_per_page": count,
                "page_num": 1,
                "query": keyword,
                "search_type": 0,
            },
        }
    }
    resp = requests.post(
        SEARCH_URL, params={"format": "json"}, json=payload, headers=HEADERS, timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    try:
        songs = data["req"]["data"]["body"]["song"]["list"]
    except (KeyError, TypeError):
        raise RuntimeError(f"Unexpected search response shape: {json.dumps(data)[:500]}")

    return [
        {"songmid": s["mid"], "name": s["name"], "singer": s["singer"][0]["name"] if s.get("singer") else "?"}
        for s in songs
    ]


def fetch_qrc_lyric(songmid: str) -> str:
    """Fetch and decrypt word-by-word (QRC) lyrics for a songmid. Falls back
    to plain LRC (base64, no decryption needed) if QRC isn't available."""
    payload = {
        "req_1": {
            "method": "GetPlayLyricInfo",
            "module": "music.musichallSong.PlayLyricInfo",
            "param": {
                "songMID": songmid,
                "songID": 0,
                "qrc": 1,
                "trans": 1,
                "roma": 1,
            },
        }
    }
    resp = requests.post(
        LYRIC_URL, params={"format": "json"}, json=payload, headers=HEADERS, timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    try:
        lyric_data = data["req_1"]["data"]
    except (KeyError, TypeError):
        raise RuntimeError(f"Unexpected lyric response shape: {json.dumps(data)[:500]}")

    qrc_hex = lyric_data.get("lyric", "")
    if not qrc_hex:
        raise RuntimeError("No lyric field in response — song may have no lyrics, or API shape changed.")

    # If it's plain base64 LRC (short, not hex), just base64-decode it.
    is_hex = bool(re.fullmatch(r"[0-9a-fA-F]+", qrc_hex))
    if is_hex and len(qrc_hex) > 100:
        return decrypt_qrc(qrc_hex)
    else:
        import base64
        return base64.b64decode(qrc_hex).decode("utf-8", errors="ignore")


def parse_qrc(xml_text: str):
    """Parse decrypted QRC markup into a list of lines, each a list of
    (word, start_ms, duration_ms) tuples. QRC line format looks like:
    [start,duration]word1(start1,dur1)word2(start2,dur2)...
    """
    lines_out = []
    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*)")
    word_pattern = re.compile(r"([^()]*)\((\d+),(\d+)\)")

    for raw_line in xml_text.splitlines():
        m = line_pattern.match(raw_line.strip())
        if not m:
            continue
        words = word_pattern.findall(m.group(3))
        if words:
            lines_out.append(
                [(w.strip(), int(start), int(dur)) for w, start, dur in words if w.strip()]
            )
    return lines_out


def main():
    if len(sys.argv) < 2:
        print("Usage: python qqmusic_lyrics.py <song name> [artist]")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Searching for: {query}\n")

    try:
        results = search_song(query)
    except Exception as e:
        print(f"Search failed: {e}")
        sys.exit(1)

    if not results:
        print("No results found.")
        sys.exit(1)

    for i, r in enumerate(results):
        print(f"  [{i}] {r['name']} - {r['singer']} (mid={r['songmid']})")

    choice = 0
    if len(results) > 1:
        try:
            choice = int(input("\nPick a result number [0]: ") or 0)
        except ValueError:
            choice = 0

    songmid = results[choice]["songmid"]
    print(f"\nFetching lyrics for songmid={songmid} ...")

    try:
        raw_lyric = fetch_qrc_lyric(songmid)
    except Exception as e:
        print(f"Lyric fetch/decrypt failed: {e}")
        sys.exit(1)

    parsed = parse_qrc(raw_lyric)

    if not parsed:
        print("\nCouldn't parse word-by-word structure — printing raw decrypted lyric instead:\n")
        print(raw_lyric[:2000])
        return

    print(f"\nParsed {len(parsed)} lines of word-by-word lyrics.\n")
    for line in parsed[:5]:
        line_str = " ".join(f"{w}[{start}]" for w, start, dur in line)
        print(line_str)
    print("\n(showing first 5 lines only)")


if __name__ == "__main__":
    main()
