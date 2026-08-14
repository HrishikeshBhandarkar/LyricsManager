# As the name suggests, this scans the specified directory and outputs supported audio files in a dictionary.
from pathlib import Path

# Comprehensive set of ALL known audio file formats on Earth:
SUPPORTED_AUDIO_EXTENSIONS = {
    # Standard Consumer & Streaming Formats
    ".mp3", ".mp2", ".mp1", ".mpa", ".m4a", ".m4b", ".m4p", ".m4r", ".aac", ".mp4",
    # Lossless PCM & Audiophile Formats
    ".flac", ".fla", ".wav", ".wave", ".bwf", ".aiff", ".aif", ".aifc", ".alac",
    # OGG, Opus & Open Codecs
    ".ogg", ".oga", ".opus", ".spx", ".ogx",
    # Windows Media, Monkey's Audio & WavPack
    ".wma", ".asf", ".ape", ".mac", ".wv", ".wvp",
    # Audiophile High-Res & Specialized Lossless
    ".tta", ".tak", ".ofr", ".ofs", ".shn", ".dsd", ".dsf", ".dff",
    # Dolby, DTS & Cinema Multi-Channel
    ".ac3", ".eac3", ".ec3", ".dts", ".dtshd", ".dtsma", ".mlp", ".truehd", ".thd",
    # Speech, Mobile & Telephony
    ".amr", ".awb", ".gsm", ".qcp", ".vox",
    # Studio, Legacy & Workstation Formats
    ".au", ".snd", ".caf", ".w64", ".rf64", ".pcm", ".raw", ".lpcm", ".voc", ".smp",
    ".sd2", ".iff", ".svx", ".8svx", ".16sv", ".paf", ".sf", ".nist", ".sph", ".avr", ".cdr", ".cda",
    # RealAudio & TwinVQ
    ".ra", ".ram", ".rm", ".vqf",
    # Audio Containers & Web Streams
    ".mka", ".webm", ".weba", ".flv", ".f4a", ".f4b", ".3gp", ".3g2", ".mov",
    # MIDI & Tracker Module Formats
    ".mid", ".midi", ".kar", ".rmi",
    ".mod", ".xm", ".it", ".s3m", ".stm", ".mtm", ".umx", ".mo3", ".669", ".far", ".okt", ".ptm",
    # Chiptune & Video Game Audio Emulation
    ".vgm", ".vgz", ".nsf", ".nsfe", ".spc", ".gym", ".gbs", ".hes", ".kss", ".ay", ".sap", ".sid",
    # Game Engine & Console Audio
    ".adx", ".hca", ".brstm", ".bcstm", ".bfstm", ".vag", ".at9", ".at3", ".xma", ".fsb", ".bnk", ".pck"
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

