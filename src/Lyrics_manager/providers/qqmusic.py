import re
from pathlib import Path

from .utils import ms_to_lrc_time_3, is_truly_enhanced


def parse_qrc_to_elrc(qrc_xml: str, is_enhanced: bool = True) -> str:
    """
    MY QQ MUSIC QRC TO REFERENCE ELRC PARSER:
    Converts decrypted QQ Music QRC XML lines into reference ELRC format matching Just Keep Watching - Tate McRae.lrc.
    - QRC Line Format: [line_start_ms, line_dur_ms]word(word_rel_start_ms, word_dur_ms)...
    - v1 Format: [00:08.010]v1:<00:08.010>Word <00:08.129>by <00:08.428>word <00:09.595>
    - bg Format: [bg:<00:09.595>Yeah, <00:09.847>yeah <00:10.919>]
    """
    if not qrc_xml:
        return ""

    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*?)(?=\[\d+,\d+\]|$)", re.S)
    word_pattern = re.compile(r"(.*?)\((\d+),(\d+)\)")

    out_lines = []

    for line_start_str, line_dur_str, body in line_pattern.findall(qrc_xml):
        line_start_ms = int(line_start_str)

        raw_words = word_pattern.findall(body)
        valid_words = [(text, int(w_start), int(w_dur)) for text, w_start, w_dur in raw_words if text.strip()]
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
                # QRC word timestamps can be absolute (>= line_start_ms) or relative
                abs_ms = w_val_ms if w_val_ms >= line_start_ms else line_start_ms + w_val_ms
                last_word_end_ms = max(last_word_end_ms, abs_ms + w_dur_ms)
                word_parts.append(f"<{ms_to_lrc_time_3(abs_ms)}>{w_str}")

            if word_parts:
                line_end_tag = f"<{ms_to_lrc_time_3(last_word_end_ms)}>"
                if is_bg:
                    out_lines.append(f"[bg:{' '.join(word_parts)} {line_end_tag}]")
                else:
                    out_lines.append(f"{line_start_tag}v1:{' '.join(word_parts)} {line_end_tag}")
        else:
            clean_line_text = "".join(w[0] for w in valid_words)
            if is_bg:
                clean_line_text = clean_line_text.strip("()\uff08\uff09")
                out_lines.append(f"[bg:{clean_line_text}]")
            else:
                out_lines.append(f"{line_start_tag} {clean_line_text}")

    return "\n".join(out_lines)


def qqmusic_provider(data: dict, type: str = "enhanced") -> str:
    """
    MY QQ MUSIC QRC PROVIDER:
    1. Uses qq_vt module functions (search_song, fetch_qrc_raw, decode_qrc) to fetch raw QRC hex blob.
    2. Decrypts QRC hex blob using 3-round DES ECB + zlib inflate into QRC XML text.
    3. Parses QRC XML into reference ELRC format matching Just Keep Watching - Tate McRae.lrc.
    """
    title = data.get("title", "")
    artist = data.get("artist", "")
    is_enhanced_flag = (type.lower() in ("enhanced", "word"))

    if not title:
        return ""

    try:
        from .qq_vt import search_song, fetch_qrc_raw, decode_qrc, fetch_plain_lrc

        search_res = search_song(title, artist)
        if search_res and search_res.get("songmid"):
            songmid = search_res["songmid"]
            songid = search_res["songid"]

            hex_blob = fetch_qrc_raw(songmid, songid)
            if hex_blob:
                qrc_xml = decode_qrc(hex_blob)
                if qrc_xml:
                    parsed_elrc = parse_qrc_to_elrc(qrc_xml, is_enhanced=is_enhanced_flag)
                    if parsed_elrc:
                        if is_enhanced_flag:
                            if is_truly_enhanced(parsed_elrc):
                                return parsed_elrc
                        else:
                            return parsed_elrc

            # Fallback to plain line LRC if QRC not available
            lrc_plain = fetch_plain_lrc(songmid)
            if lrc_plain:
                return lrc_plain
    except Exception:
        pass

    return ""
