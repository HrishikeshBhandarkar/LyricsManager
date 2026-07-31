import requests
def fetch_lrc(name : str,artist_name : str):
    baseURL="https://lrclib.net/api/get"
    params = { 
        "track_name" : name,
        "artist_name" : artist_name
          }
    print(f"Searching for lyrics of the song {name} by {artist_name} in LRCLIB be patient")
    try:
        response=requests.get(baseURL,params=params,timeout=5)
        if response.status_code==200:
            output = response.json()
            syncedLyrics=output.get("syncedLyrics")
            if syncedLyrics :
                print("Lyrics found and heres the preview")
                lines=syncedLyrics.splitlines()[:10]
                for i in lines:
                    print(i)
                print("-----------------\n")
            else:
                print("Lyrics found but not LineSynced")
    except: 
        return print("Error")
if __name__ == "__main__":
    # Test with any song you like!
    fetch_lrc("Numb", "Linkin Park")

