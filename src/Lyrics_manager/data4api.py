import mutagen
from pathlib import Path

def get_params(result: dict[int, dict]) -> tuple[dict, dict]:
    """
    Reads audio metadata (title, artist) from selected track files using Mutagen.
    If tags are missing, attempts a filename fallback (e.g. 'Artist - Title').
    Returns two dictionaries: (parsed_tracks, failed_tracks).
    """
    parsed_tracks = {}
    failed_tracks = {}

    # FIX 1: Iterating over key-value pairs (track_id, track_info) instead of 'for i in result'.
    # In my previous code, 'for i in result' gave me integer keys (1, 2, 3...), so doing i["path"] crashed with a TypeError.
    for track_id, track_info in result.items():
        file_path = Path(track_info["path"])

        if not file_path.exists():
            failed_tracks[track_id] = {
                "path": file_path,
                "reason": "File does not exist"
            }
            continue

        audio = None
        duration_ms = 0
        title = None
        artist = None

        try:
            audio = mutagen.File(file_path, easy=True)
            if audio is not None:
                if "title" in audio and audio["title"]:
                    title = str(audio["title"][0]).strip()
                if "artist" in audio and audio["artist"]:
                    artist = str(audio["artist"][0]).strip()
                if audio.info and hasattr(audio.info, "length"):
                    duration_ms = int(float(audio.info.length) * 1000)
        except Exception:
            audio = None

        # Filename fallback logic for missing tags or unsupported metadata formats
        if not title or not artist:
            stem_name = file_path.stem
            
            # If filename contains a hyphen (e.g. 'Artist - Title'), split on the FIRST hyphen only
            if "-" in stem_name:
                parts = stem_name.split("-", 1)
                if not artist:
                    artist = parts[0].strip()
                if not title:
                    title = parts[1].strip()
            else:
                if not title:
                    title = stem_name.strip()
                if not artist:
                    artist = "Unknown Artist"

        parsed_tracks[track_id] = {
            "title": title or file_path.stem,
            "artist": artist or "Unknown Artist",
            "path": file_path,
            "duration_ms": duration_ms
        }

    return parsed_tracks, failed_tracks


if __name__ == "__main__":
    # Small test block to verify metadata extraction works on sample files
    test_data = {
        1: {"path": r"C:\Users\hrish\Samples\Joji - PIXELATED KISSES.flac"}
    }
    parsed, failed = get_params(test_data)
    print("Parsed Tracks:", parsed)
    print("Failed Tracks:", failed)
