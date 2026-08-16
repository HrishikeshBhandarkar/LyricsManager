# As the name suggests, this scans the specified directory and outputs supported audio files in a dictionary.
from pathlib import Path

# Supported core audio formats:
SUPPORTED_AUDIO_EXTENSIONS = {
    ".m4a",
    ".mp3",
    ".flac",
    ".alac",
    ".aac",
    ".webm",
}

def scan(Directory: str) -> dict[int, dict]:
    """
    Scans the given directory recursively for ALL supported audio files.
    Returns a dictionary mapping 1-based index integers to track metadata dictionaries:
    {
        1: {'path': Path(...), 'name': 'song.mp3', 'stem': 'song', 'suffix': '.mp3'},
        ...
    }
    """
    data = {}
    dic_t = Path(Directory)
    
    if not dic_t.is_dir():
        print(f"The path {Directory} is not valid")
        return {}

    # Scan and sort files alphabetically to ensure consistent index ordering
    audio_files = sorted([
        item for item in dic_t.rglob("*")
        if item.is_file() and item.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    ])

    for index, item in enumerate(audio_files, start=1):
        data[index] = {
            "path": item.resolve(),
            "name": item.name,
            "stem": item.stem,
            "suffix": item.suffix.lower()
        }

    return data

if __name__ == "__main__":
    k = input("Enter a path = ")
    found_files = scan(k)
    print(f"Found {len(found_files)} audio file(s):")
    for idx, track in found_files.items():
        print(f" [{idx}] {track['name']} -> {track['path']}")

