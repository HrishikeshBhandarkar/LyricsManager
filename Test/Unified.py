import base64
import json
import zlib
import requests
from Crypto.Cipher import DES

# QQ Music static DES key for QRC lyrics
QRC_DES_KEY = b"!@#$0%&*"


def decrypt_qrc(raw_encrypted_str: str) -> str:
    """Decrypts QQ Music QRC payload (Hex or Base64) -> DES ECB -> Zlib Inflate."""
    # 1. Convert string representation to raw bytes
    try:
        # Check if hex-encoded
        encrypted_bytes = bytes.fromhex(raw_encrypted_str)
    except ValueError:
        # Fallback to base64 if not hex
        encrypted_bytes = base64.b64decode(raw_encrypted_str)

    # 2. DES ECB Decryption
    cipher = DES.new(QRC_DES_KEY, DES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # 3. Zlib Decompression
    try:
        decompressed_data = zlib.decompress(decrypted_bytes)
        return decompressed_data.decode("utf-8", errors="replace")
    except zlib.error as e:
        raise ValueError("Failed to decompress decrypted QRC bytes.") from e


def fetch_qq_word_lyrics(song_mid: str) -> str:
    """Fetches and decrypts word-by-word QRC lyrics for a given songMID."""
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"

    payload = {
        "comm": {
            "cv": 4747474,
            "ct": 24,
            "format": "json", "inCharset": "utf-8",
            "outCharset": "utf-8",
        },
        "req_0": {
            "module": "music.musichallSong.PlayLyricInfo",
            "method": "GetPlayLyricInfo",
            "param": {
                "songMID": song_mid,
                "qrc": 1,
                "qrc_t": 0,
                "roma": 1,
                "trans": 1,
            },
        },
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://y.qq.com/",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    lyric_info = data.get("req_0", {}).get("data", {})

    # QRC data can reside under 'qrc' or 'lyric' key depending on API variant
    raw_qrc = lyric_info.get("qrc") or lyric_info.get("lyric")

    if not raw_qrc:
        raise RuntimeError(
            "No QRC word-level lyrics found for this track. "
            "It might only have standard line LRC available."
        )

    return decrypt_qrc(raw_qrc)


if __name__ == "__main__":
    # Example songMID (e.g., "003OUAho21A2a1")
    target_song_mid = "003OUAho21A2a1"

    try:
        qrc_content = fetch_qq_word_lyrics(target_song_mid)
        print("--- Decrypted QRC Word-by-Word Lyrics ---\n")
        print(qrc_content[:500])  # Print first 500 characters
    except Exception as err:
        print(f"Error fetching lyrics: {err}")