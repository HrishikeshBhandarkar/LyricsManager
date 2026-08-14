"""
MY AI ELRC BUILDER MODULE (STRICT LINE-PRESERVING VERSION):
Converts word alignment segments into reference ELRC formatted strings matching Just Keep Watching - Tate McRae.lrc.
RULES:
1. STRICT 1:1 Line Preservation: Each line in the input transcript remains EXACTLY one line in the output ELRC.
   No merging multiple transcript lines into one, and no splitting a transcript line into two!
2. Header Tags: [ti:...], [ar:...], [offset:+0], [by:Generated using LyricsManager (AI Forced Alignment)]
3. 3-Decimal Timestamps: [MM:SS.mmm] and <MM:SS.mmm>
4. Main Vocal Lines: [MM:SS.mmm]v1:<MM:SS.mmm>Word <MM:SS.mmm>by ... <MM:SS.mmm>
5. Background Vocal Lines: [bg:<MM:SS.mmm>Yeah, <MM:SS.mmm>yeah ... <MM:SS.mmm>]
"""

def ms_to_lrc_time_3(ms: int) -> str:
    minutes = ms // 60000
    seconds = (ms % 60000) / 1000.0
    return f"{minutes:02d}:{seconds:06.3f}"

def _parse_speaker_and_clean_text(line_text: str):
    """Extract explicit v1:/v2: prefix if it exists, determine bg flag, and return cleaned text and speaker."""
    lower_line = line_text.lower()
    explicit_speaker = None
    
    if lower_line.startswith("v1:") or lower_line.startswith("v1 :"):
        explicit_speaker = "v1"
        line_text = line_text.split(":", 1)[1].strip()
    elif lower_line.startswith("v2:") or lower_line.startswith("v2 :"):
        explicit_speaker = "v2"
        line_text = line_text.split(":", 1)[1].strip()

    is_bg = line_text.startswith("(") or line_text.startswith("（") or line_text.startswith("[bg:")
    speaker = explicit_speaker if explicit_speaker else "v1"
    
    return line_text, speaker, is_bg


def build_lrc_lines(lines_with_words: list[dict], title: str = "", artist: str = "") -> str:
    if not lines_with_words:
        return ""

    header_lines = []
    if title:
        header_lines.append(f"[ti:{title}]")
    if artist:
        header_lines.append(f"[ar:{artist}]")
    header_lines.append("[offset:+0]")
    header_lines.append("[by:Generated using LyricsManager (AI Forced Alignment)]")

    content_lines = []

    for line_data in lines_with_words:
        raw_text = line_data.get("line_text", "").strip()
        words = line_data.get("words", [])

        if not raw_text:
            continue
            
        line_text, speaker, is_bg = _parse_speaker_and_clean_text(raw_text)
        
        valid_words = [w for w in words if w.get("word", "").strip()]
        
        if valid_words:
            line_start_ms = int(valid_words[0]["start"] * 1000)
            line_start_tag = f"[{ms_to_lrc_time_3(line_start_ms)}]"
            if is_bg:
                content_lines.append(f"{line_start_tag}[bg:{line_text}]")
            else:
                # Standard LRC doesn't usually use v1/v2 tags, but if we want to preserve them:
                # We can output the raw text or the parsed text. The user requested:
                # "just keep name everything as V1 except for the parenthesis that is the BG block... 
                # Only do only assign V1 and V2 if the transcript is given itself like V1 : the letters"
                prefix = f"{speaker}:" if speaker != "v1" else ""
                content_lines.append(f"{line_start_tag}{prefix}{line_text}")
        else:
            if is_bg:
                content_lines.append(f"[00:00.000] [bg:{line_text}]")
            else:
                prefix = f"{speaker}:" if speaker != "v1" else ""
                content_lines.append(f"[00:00.000] {prefix}{line_text}")

    return "\n".join(header_lines + content_lines)



def build_elrc_strict_lines(lines_with_words: list[dict], title: str = "", artist: str = "") -> str:
    """
    Converts list of transcript line dicts:
    [
        {
            "line_text": "Pixelated kisses got me goin' insane",
            "words": [{"word": "Pixelated", "start": 1.2, "end": 1.8}, ...]
        },
        ...
    ]
    strictly preserving 1 line in input = 1 line in output ELRC.
    """
    if not lines_with_words:
        return ""

    header_lines = []
    if title:
        header_lines.append(f"[ti:{title}]")
    if artist:
        header_lines.append(f"[ar:{artist}]")
    header_lines.append("[offset:+0]")
    header_lines.append("[by:Generated using LyricsManager (AI Forced Alignment)]")

    content_lines = []

    for line_data in lines_with_words:
        raw_text = line_data.get("line_text", "").strip()
        words = line_data.get("words", [])

        if not raw_text:
            continue

        line_text, speaker_tag, is_bg = _parse_speaker_and_clean_text(raw_text)

        # If aligned words exist for this line
        valid_words = [w for w in words if w.get("word", "").strip()]
        
        if valid_words:
            line_start_ms = int(valid_words[0]["start"] * 1000)
            line_end_ms = int(valid_words[-1]["end"] * 1000)

            word_parts = []
            for w in valid_words:
                w_start_ms = int(w["start"] * 1000)
                # Strip v1:/v2: from the first word if it was passed into the word alignments
                clean_w = w["word"].strip("()（）") if is_bg else w["word"]
                if clean_w.lower().startswith("v1:") or clean_w.lower().startswith("v2:"):
                    clean_w = clean_w.split(":", 1)[1].strip()
                word_parts.append(f"<{ms_to_lrc_time_3(w_start_ms)}>{clean_w}")

            line_start_tag = f"[{ms_to_lrc_time_3(line_start_ms)}]"
            line_end_tag = f"<{ms_to_lrc_time_3(line_end_ms)}>"

            if is_bg:
                content_lines.append(f"[bg:{' '.join(word_parts)} {line_end_tag}]")
            else:
                content_lines.append(f"{line_start_tag}{speaker_tag}:{' '.join(word_parts)} {line_end_tag}")
        else:
            # Unaligned line fallback (use line text without word timestamps)
            if is_bg:
                content_lines.append(f"[bg:{line_text}]")
            else:
                content_lines.append(f"[00:00.000] {speaker_tag}:{line_text}")

    return "\n".join(header_lines + content_lines)
