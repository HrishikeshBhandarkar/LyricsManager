"""
Lyric Manager - Metadata Tag Embedder Module
Handles embedding lyrics directly into audio metadata tags across supported audio formats:
M4A, MP3, FLAC, ALAC, AAC, WebM.
"""
from pathlib import Path
import mutagen
from mutagen.id3 import ID3, USLT, ID3NoHeaderError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4


def embed_lyrics(file_path: Path | str, lyrics: str) -> bool:
    """
    Embeds lyrics into audio file metadata tags based on audio format.
    - MP3: ID3 USLT frame
    - FLAC: Vorbis comment LYRICS tag
    - M4A / ALAC / AAC / MP4: MP4 atom ©lyr
    - WebM / Fallback: Vorbis comment LYRICS tag / mutagen.File
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

        elif suffix in (".flac",):
            audio = mutagen.File(path)
            if audio is not None:
                audio["LYRICS"] = lyrics
                audio.save()
                return True

        elif suffix in (".m4a", ".alac", ".aac", ".mp4"):
            try:
                audio = MP4(path)
                audio["\xa9lyr"] = [lyrics]
                audio.save()
                return True
            except Exception:
                audio = mutagen.File(path)
                if audio is not None:
                    audio["\xa9lyr"] = [lyrics]
                    audio.save()
                    return True

        else:
            # Fallback for WebM or other formats via mutagen
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
