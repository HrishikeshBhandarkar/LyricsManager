import re
import zlib
import base64
import requests
from pathlib import Path

from .utils import ms_to_lrc_time, is_truly_enhanced


# MY KUGOU KRC ENCRYPTION KEY:
# Fixed 16-byte XOR key used to decrypt KuGou KRC word-by-word lyric payloads.
KRC_ENCODE_KEY = bytes([64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105])


def decode_krc(content: bytes) -> str:
    """
    MY KRC DECRYPTION HELPER:
    Strips the 4-byte KRC header magic, XOR-decrypts remaining bytes with KRC_ENCODE_KEY,
    and inflates using zlib.decompress().
    """
    # Strip 4-byte header prefix
    payload = content[4:]
    # XOR decrypt bytes using fixed 16-byte key cyclically
    decrypted = bytes(b ^ KRC_ENCODE_KEY[i % 16] for i, b in enumerate(payload))
    # Decompress binary stream via zlib inflate into UTF-8 text string
    return zlib.decompress(decrypted).decode("utf-8", errors="ignore")


def parse_krc_to_elrc(krc_text: str, is_enhanced: bool = True) -> str:
    """
    MY KRC TO ELRC PARSER & FORMATTER:
    Converts decrypted KuGou KRC markup lines into standardized ELRC format.
    - KRC Line Format: [line_start_ms, line_dur_ms]<word_start_ms, word_dur_ms, 0>WordText...
    - Output Format: [MM:SS.xx][v1]Word<MM:SS.xx>by<MM:SS.xx>word...
    - Supports background vocal tags [bg] for parenthesized text.
    """
    if not krc_text:
        return ""

    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*)")
    word_pattern = re.compile(r"<(\d+),(\d+),\d+>([^<]*)")

    out_lines = []

    for raw_line in krc_text.splitlines():
        line_match = line_pattern.match(raw_line.strip())
        if not line_match:
            continue

        line_start_ms = int(line_match.group(1))
        content_str = line_match.group(3)

        words = word_pattern.findall(content_str)
        valid_words = [(text, int(start), int(dur)) for start, dur, text in words if text.strip()]
        if not valid_words:
            continue

        # Check if entire line is wrapped in parentheses indicating background vocals
        joined_text = "".join(w[0] for w in valid_words).strip()
        is_bg = joined_text.startswith("(") or joined_text.startswith("\uff08")

        # Format line start timestamp in MM:SS.xx and voice tag with trailing space
        line_start_tag = f"[{ms_to_lrc_time(line_start_ms)}]"
        voice_tag = "[bg][v1] " if is_bg else "[v1] "

        if is_enhanced:
            word_parts = []
            last_word_end_ms = line_start_ms
            for text, word_rel_ms, dur_ms in valid_words:
                clean_w = text.strip("()\uff08\uff09") if is_bg else text
                w_str = clean_w.strip()
                if not w_str:
                    continue
                abs_ms = line_start_ms + word_rel_ms
                last_word_end_ms = max(last_word_end_ms, abs_ms + dur_ms)
                # Place timestamp tag BEFORE word text e.g. <00:00.00>Numb
                word_parts.append(f"<{ms_to_lrc_time(abs_ms)}>{w_str}")
            if word_parts:
                line_end_tag = f"<{ms_to_lrc_time(last_word_end_ms)}>"
                out_lines.append(f"{line_start_tag}{voice_tag}{' '.join(word_parts)} {line_end_tag}")
        else:
            clean_line_text = "".join(w[0] for w in valid_words)
            if is_bg:
                clean_line_text = clean_line_text.strip("()\uff08\uff09 ")
            out_lines.append(f"{line_start_tag} {clean_line_text}")

    return "\n".join(out_lines)


def kugou_provider(data: dict, type: str = "enhanced") -> str:
    """
    MY KUGOU KRC SYLLABLE-LEVEL LYRIC PROVIDER:
    1. Reads track duration directly from input data["duration_ms"] or calculates it via Mutagen from audio file.
    2. Queries KuGou search API (http://lyrics.kugou.com/search) with track name, artist, and duration.
    3. Downloads encrypted KRC payload from http://lyrics.kugou.com/download.
    4. Decrypts KRC using XOR key + zlib inflate and formats into ELRC/LRC strings.
    """
    title = data.get("title", "")
    artist = data.get("artist", "")
    path = data.get("path")
    is_enhanced_flag = (type.lower() in ("enhanced", "word"))

    if not title or not artist:
        return ""

    # Determine song duration in milliseconds directly from input metadata or local audio file header
    duration_ms = data.get("duration_ms", 0)
    if not duration_ms and path and Path(path).exists():
        try:
            import mutagen
            audio = mutagen.File(path, easy=True)
            if audio and audio.info and hasattr(audio.info, "length"):
                duration_ms = int(float(audio.info.length) * 1000)
        except Exception:
            duration_ms = 0

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    search_url = "http://lyrics.kugou.com/search"
    download_url = "http://lyrics.kugou.com/download"

    # Define query attempts with duration and fallback variations
    attempts = [
        {"keyword": f"{title} - {artist}", "duration": duration_ms},
        {"keyword": f"{artist} - {title}", "duration": duration_ms},
        {"keyword": f"{title} {artist}", "duration": duration_ms},
        {"keyword": f"{title} - {artist}", "duration": 0},
    ]

    candidates = []
    for attempt in attempts:
        try:
            res = requests.get(
                search_url,
                params={"ver": 1, "man": "yes", "client": "pc", **attempt},
                headers=headers,
                timeout=6,
            )
            if res.status_code == 200:
                data_json = res.json()
                cand = data_json.get("candidates", [])
                if cand:
                    candidates = cand
                    break
        except Exception:
            continue

    if not candidates:
        return ""

    # Pick top matching candidate from KuGou candidate list
    picked = candidates[0]
    lyric_id = picked.get("id")
    accesskey = picked.get("accesskey")

    if not lyric_id or not accesskey:
        return ""

    try:
        res = requests.get(
            download_url,
            params={"ver": 1, "client": "pc", "id": lyric_id, "accesskey": accesskey, "fmt": "krc", "charset": "utf8"},
            headers=headers,
            timeout=6,
        )
        if res.status_code == 200:
            data_json = res.json()
            content_b64 = data_json.get("content")
            if content_b64:
                raw_bytes = base64.b64decode(content_b64)
                krc_text = decode_krc(raw_bytes)

                parsed_elrc = parse_krc_to_elrc(krc_text, is_enhanced=is_enhanced_flag)

                if parsed_elrc:
                    if is_enhanced_flag:
                        if is_truly_enhanced(parsed_elrc):
                            return parsed_elrc
                    else:
                        return parsed_elrc
    except Exception:
        return ""

    return ""
