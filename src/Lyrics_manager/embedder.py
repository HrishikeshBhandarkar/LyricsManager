"""
MY EMBEDDER MODULE:
Handles embedding lyrics directly into audio metadata tags across a comprehensive set of audio formats using Mutagen.
Supported formats: MP3, FLAC, M4A/MP4/AAC, OGG/Opus/OGA, WAV, AIFF, WMA/ASF, APE, WavPack.
"""
from pathlib import Path
import mutagen
from mutagen.id3 import ID3, USLT, ID3NoHeaderError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from mutagen.asf import ASF


def embed_lyrics(file_path: Path | str, lyrics: str) -> bool:
    """
    MY EMBEDDER FUNCTION:
    Embeds lyrics into audio file metadata tags based on audio container format.
    - MP3 / AIFF / WAV: ID3 USLT (Unsynchronised Lyric) frame
    - FLAC / OGG / Opus / OGA: Vorbis comment LYRICS tag
    - M4A / MP4 / AAC: MP4 atom \xa9lyr
    - WMA / ASF: WM/Lyrics tag
    Returns True if embedding succeeded, False otherwise.
    """
    path = Path(file_path)
    if not path.exists() or not lyrics:
        return False

    suffix = path.suffix.lower()

    try:
        if suffix == ".mp3":
            try:
                tags = ID3(path)
            except ID3NoHeaderError:
                tags = ID3()
            tags.add(USLT(encoding=3, lang="eng", desc="", text=lyrics))
            tags.save(path)
            return True

        elif suffix in (".flac", ".ogg", ".opus", ".oga"):
            audio = mutagen.File(path)
            if audio is not None:
                audio["LYRICS"] = lyrics
                audio.save()
                return True

        elif suffix in (".m4a", ".mp4", ".aac"):
            audio = MP4(path)
            audio["\xa9lyr"] = [lyrics]
            audio.save()
            return True

        elif suffix in (".aiff", ".aif", ".aifc"):
            audio = AIFF(path)
            if audio.tags is None:
                audio.add_tags()
            audio.tags.add(USLT(encoding=3, lang="eng", desc="", text=lyrics))
            audio.save()
            return True

        elif suffix == ".wav":
            try:
                audio = WAVE(path)
                if audio.tags is None:
                    audio.add_tags()
                audio.tags.add(USLT(encoding=3, lang="eng", desc="", text=lyrics))
                audio.save()
                return True
            except Exception:
                audio = mutagen.File(path)
                if audio is not None:
                    audio["lyrics"] = lyrics
                    audio.save()
                    return True

        elif suffix in (".wma", ".asf"):
            audio = ASF(path)
            audio["WM/Lyrics"] = lyrics
            audio.save()
            return True

        else:
            # Fallback for any other format supported by Mutagen (e.g. APE, WavPack)
            audio = mutagen.File(path)
            if audio is not None:
                try:
                    audio["LYRICS"] = lyrics
                    audio.save()
                    return True
                except Exception:
                    pass
                audio["lyrics"] = lyrics
                audio.save()
                return True

    except Exception as e:
        print(f"Error embedding lyrics into {path.name}: {e}")
        return False

    return False
