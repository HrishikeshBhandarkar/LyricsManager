from pathlib import Path
import mutagen
def metadata(fpath : str):
    path = Path(fpath)
    if not path.exists():
        print(f"The provided path {fpath} dosent exist")
        return None
    try:
        audio = mutagen.File(path)
        if audio is None:
            print("The file {fpath} might be curropted")
            return None
        title = None
        artist = None
        if 'TIT2' in audio:
            title = str(audio['TIT2'][0])
        elif 'tittle' in audio:
            title = str(audio['title'][0])
        if 'TPE1' in audio:
            artist=str(audio['TPE1'][0])
        elif 'artist' in audio:
            artist = str(audio['artist'][0])
        if title == None:
            title = path.stem
        if artist==None:
            artist = "Unknown Artist"
        duration = int(audio.info.length) if audio.info else 0
        print("--MetaData extracted--")
        print(f"Title : {title}")
        print(f"Artist : {artist}")
        print(f"Length  : {duration} seconds ({duration // 60}:{duration % 60:02d})")
        return {"title" : title, "artist" : artist, "duration":duration}
    except Exception as e:
        print(f"Error reading the metadata {e}")
        return None


if __name__=="__main__":
    x=r"C:\Users\hrish\Lyric_manager\Test\Samples\Joji - PIXELATED KISSES.flac"
    metadata(x)
