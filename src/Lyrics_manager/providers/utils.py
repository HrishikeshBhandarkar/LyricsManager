import re


def ms_to_lrc_time(ms: int) -> str:
    """
    MY TIMESTAMP CONVERTER HELPER:
    Converts integer milliseconds (e.g. 4690 ms) into standard LRC timestamp string 'MM:SS.xx'.
    - ms / 1000.0 converts ms to float seconds.
    - seconds // 60 computes total whole minutes.
    - seconds % 60 computes remaining whole seconds.
    - (seconds % 1) * 100 computes 2-digit hundredths of a second.
    """
    seconds = ms / 1000.0
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    hundredths = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{hundredths:02d}"


def ms_to_lrc_time_3(ms: int) -> str:
    """
    MY TIMESTAMP FORMATTER FOR 3-DECIMAL PRECISION:
    Converts integer milliseconds to MM:SS.mmm format e.g. 00:08.010 matching Just Keep Watching - Tate McRae.lrc.
    """
    minutes = ms // 60000
    seconds = (ms % 60000) / 1000.0
    return f"{minutes:02d}:{seconds:06.3f}"


def is_truly_enhanced(elrc_text: str) -> bool:
    r"""
    MY ENHANCED VALIDATOR:
    Verifies that word timestamps <MM:SS.xx> or <MM:SS.xxx> actually represent true word-by-word sync.
    Discards fake enhanced lyrics like '[00:45.00]<00:45.00> Hello people' returned by some APIs.
    - Checks if lines contain multiple distinct word timestamps.
    - Handles short tracks, single-line samples, and full songs dynamically.
    """
    if not elrc_text:
        return False
        
    lines = [ln.strip() for ln in elrc_text.splitlines() if ln.strip() and not ln.startswith(("[ti:", "[ar:", "[al:", "[by:", "[offset:"))]
    if not lines:
        return False
        
    multi_word_lines = 0
    all_word_timestamps = []
    
    for line in lines:
        word_timestamps = re.findall(r"<\d{2}:\d{2}\.\d{2,3}>", line)
        if len(word_timestamps) > 1:
            multi_word_lines += 1
        all_word_timestamps.extend(word_timestamps)
        
    # If the text has 1-2 lines, at least 1 multi-word line proves true ELRC
    if len(lines) <= 2:
        return multi_word_lines >= 1
        
    # For standard songs, require at least 2 multi-word lines or higher unique timestamps count
    return multi_word_lines >= 2 or len(set(all_word_timestamps)) > len(lines)
