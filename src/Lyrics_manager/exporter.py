"""
MY EXPORTER MODULE:
Handles downloading/saving separate sidecar lyric files (.lrc or .elrc) in the exact same directory as the audio track.
"""
import os
import re
from pathlib import Path
from mutagen.flac import FLAC
from mutagen.id3 import ID3, USLT, SYLT, Encoding

from .providers.utils import is_truly_enhanced


def save_lyric_file(file_path: Path | str, lyrics: str) -> Path | None:
    """
    MY EXPORTER FUNCTION:
    Saves lyrics as a separate .elrc (word-by-word) or .lrc (line-synced) sidecar file in the audio track's folder.
    Returns the Path to the generated lyric file if successful, or None if failed.
    """
    path = Path(file_path)
    if not path.exists() or not lyrics:
        return None

    try:
        is_enh = is_truly_enhanced(lyrics)
        ext = ".elrc" if is_enh else ".lrc"
        out_path = path.with_suffix(ext)
        out_path.write_text(lyrics, encoding="utf-8")
        return out_path
    except Exception as e:
        print(f"Error saving sidecar lyric file for {path.name}: {e}")
        return None
