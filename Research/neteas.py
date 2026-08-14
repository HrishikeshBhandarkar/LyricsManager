import requests
import json
import urllib.parse

class NetEaseLyricsFetcher:
    def __init__(self):
        # We spoof a standard PC browser User-Agent so they don't block us
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com'
        }

    def search_song(self, keyword):
        """Searches NetEase and returns the ID of the first match."""
        print(f"Searching NetEase for: '{keyword}'...")
        
        url = 'https://music.163.com/api/search/get'
        payload = {
            's': keyword,
            'type': 1, # 1 means search for tracks
            'limit': 1, # Just grab the top result
            'offset': 0
        }
        
        try:
            # We use POST for the search endpoint
            response = requests.post(url, headers=self.headers, data=payload)
            data = response.json()
            
            if data['code'] == 200 and 'songs' in data['result']:
                song_info = data['result']['songs'][0]
                song_id = song_info['id']
                song_name = song_info['name']
                artist_name = song_info['artists'][0]['name']
                print(f"Found: {song_name} by {artist_name} (ID: {song_id})")
                return song_id
            else:
                print("No songs found matching that query.")
                return None
                
        except Exception as e:
            print(f"Search failed: {e}")
            return None

    def get_word_by_word_lyrics(self, song_id):
        """Fetches the YRC (word-by-word) lyrics format for a given ID."""
        print(f"Fetching YRC lyrics for ID: {song_id}...")
        
        # The key parameter here is 'yv=-1'. 
        # This tells NetEase to return the YRC word-by-word timing.
        # lv=-1 (standard lrc), tv=-1 (translation), yv=-1 (word-by-word)
        url = f'https://music.163.com/api/song/lyric?id={song_id}&lv=-1&tv=-1&yv=-1&kv=-1'
        
        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            if data['code'] == 200:
                # Check if YRC (word-by-word) data actually exists for this song
                if 'yrc' in data and 'lyric' in data['yrc']:
                    yrc_lyrics = data['yrc']['lyric']
                    print("\n--- Word-by-Word (YRC) Lyrics Found! ---\n")
                    print(yrc_lyrics)
                    return yrc_lyrics
                
                # Fallback to standard LRC if word-by-word isn't available
                elif 'lrc' in data and 'lyric' in data['lrc']:
                    print("\nWord-by-word not available. Returning standard LRC timing:\n")
                    return data['lrc']['lyric']
                else:
                    print("This song is marked as instrumental or has no lyrics.")
                    return None
            else:
                print("Failed to fetch from lyrics endpoint.")
                return None
                
        except Exception as e:
            print(f"Failed to fetch lyrics: {e}")
            return None

# --- Usage Example ---
if __name__ == "__main__":
    # You will need to pip install requests if you haven't already
    fetcher = NetEaseLyricsFetcher()
    
    # Let's search for the Basco song we were looking at earlier
    query = "Titli Chinmayi Sripadar"
    
    song_id = fetcher.search_song(query)
    
    if song_id:
        lyrics = fetcher.get_word_by_word_lyrics(song_id)

