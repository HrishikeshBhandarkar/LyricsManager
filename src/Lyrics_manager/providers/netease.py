import re
import requests

from .utils import ms_to_lrc_time_3, is_truly_enhanced


def parse_yrc_to_elrc(yrc_text: str, is_enhanced: bool = True) -> str:
    """
    MY NETEASE YRC TO REFERENCE ELRC PARSER:
    Converts NetEase YRC word-by-word lines into reference ELRC format matching Just Keep Watching - Tate McRae.lrc.
    - YRC Line Format: [line_start_ms, line_dur_ms](word_start_ms, word_dur_ms, 0)WordText...
    - v1 Format: [00:08.010]v1:<00:08.010>Word <00:08.129>by <00:08.428>word <00:09.595>
    - bg Format: [bg:<00:09.595>Yeah, <00:09.847>yeah <00:10.919>]
    """
    if not yrc_text:
        return ""

    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*)", re.M)
    word_pattern = re.compile(r"\((\d+),(\d+),\d+\)([^\(\[\n]+)")

    out_lines = []

    for line_start_str, line_dur_str, body in line_pattern.findall(yrc_text):
        line_start_ms = int(line_start_str)

        raw_words = word_pattern.findall(body)
        valid_words = [(text, int(w_start), int(w_dur)) for w_start, w_dur, text in raw_words if text.strip()]
        if not valid_words:
            continue

        # Check if line text is wrapped in parentheses indicating background vocals
        joined_text = "".join(w[0] for w in valid_words).strip()
        is_bg = joined_text.startswith("(") or joined_text.startswith("\uff08")

        line_start_tag = f"[{ms_to_lrc_time_3(line_start_ms)}]"

        if is_enhanced:
            word_parts = []
            last_word_end_ms = line_start_ms
            for text, w_val_ms, w_dur_ms in valid_words:
                clean_w = text.strip("()\uff08\uff09") if is_bg else text
                w_str = clean_w.strip()
                if not w_str:
                    continue
                abs_ms = w_val_ms if w_val_ms >= line_start_ms else line_start_ms + w_val_ms
                last_word_end_ms = max(last_word_end_ms, abs_ms + w_dur_ms)
                word_parts.append(f"<{ms_to_lrc_time_3(abs_ms)}>{w_str}")

            if word_parts:
                line_end_tag = f"<{ms_to_lrc_time_3(last_word_end_ms)}>"
                joined_words = " ".join(word_parts)
                if is_bg:
                    out_lines.append(f"[bg:{joined_words} {line_end_tag}]")
                else:
                    out_lines.append(f"{line_start_tag}v1:{joined_words} {line_end_tag}")
        else:
            clean_line_text = "".join(w[0] for w in valid_words)
            if is_bg:
                clean_line_text = clean_line_text.strip("()\uff08\uff09")
                out_lines.append(f"[bg:{clean_line_text}]")
            else:
                out_lines.append(f"{line_start_tag} {clean_line_text}")

    return "\n".join(out_lines)


def netease_provider(data: dict, type: str = "enhanced") -> str:
    """
    MY NETEASE YRC PROVIDER:
    1. Connects to NetEase Music API (music.163.com/api/search/get) to find track ID.
    2. Fetches YRC (word-by-word) or LRC payload from music.163.com/api/song/lyric.
    3. Converts YRC markup into reference ELRC format matching Just Keep Watching - Tate McRae.lrc.
    """
    title = data.get("title", "")
    artist = data.get("artist", "")
    is_enhanced_flag = (type.lower() in ("enhanced", "word"))

    if not title:
        return ""

    query = f"{title} {artist}".strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://music.163.com/",
        "Host": "music.163.com"
    }

    try:
        # Step 1: Search track ID
        search_res = requests.post(
            "https://music.163.com/api/search/get",
            headers=headers,
            data={"s": query, "type": 1, "limit": 1, "offset": 0},
            timeout=5
        ).json()

        if search_res.get("code") == 200 and search_res.get("result", {}).get("songs"):
            song_id = search_res["result"]["songs"][0]["id"]

            # Step 2: Download YRC / LRC lyric payload
            lyr_res = requests.get(
                f"https://music.163.com/api/song/lyric?id={song_id}&lv=-1&tv=-1&yv=-1&kv=-1",
                headers=headers,
                timeout=5
            ).json()

            if lyr_res.get("code") == 200:
                # Priority: Word-by-Word YRC
                if "yrc" in lyr_res and lyr_res["yrc"].get("lyric"):
                    raw_yrc = lyr_res["yrc"]["lyric"]
                    parsed_elrc = parse_yrc_to_elrc(raw_yrc, is_enhanced=is_enhanced_flag)
                    if parsed_elrc:
                        if is_enhanced_flag:
                            if is_truly_enhanced(parsed_elrc):
                                return parsed_elrc
                        else:
                            return parsed_elrc
                # Line-Synced LRC Fallback
                elif "lrc" in lyr_res and lyr_res["lrc"].get("lyric"):
                    return lyr_res["lrc"]["lyric"]
    except Exception:
        pass

    return ""
