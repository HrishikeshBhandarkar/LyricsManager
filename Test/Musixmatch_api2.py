import time
import requests
import json
from typing import Optional, Dict, Any, Tuple
#This script is working but remember to save the tokens as srveral token requests can block the ip of the user then understand this code 
class Musixmatch:
    ROOT_URL = "https://apic-desktop.musixmatch.com/ws/1.1/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.musixmatch.com",
            "Referer": "https://www.musixmatch.com/",
        })
        self.token: Optional[str] = None
        self.token_retry_count = 0
        self.token_retry_max = 3

    def _get(self, action: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Internal helper to make API requests with default parameters and handling."""
        params["app_id"] = "web-desktop-app-v1.0"
        
        if self.token and action != "token.get":
            params["usertoken"] = self.token

        params["t"] = str(int(time.time() * 1000))
        url = self.ROOT_URL + action

        response = self.session.get(url, params=params, allow_redirects=True)
        response.raise_for_status()
        
        return response.json()

    def get_token(self, force: bool = False) -> None:
        """Retrieves and sets the user authentication token."""
        if self.token is None and self.token_retry_count < self.token_retry_max:
            data = self._get("token.get", {"user_language": "en"})
            self.token_retry_count += 1
            
            status_code = data.get("message", {}).get("header", {}).get("status_code")
            if status_code == 401:
                raise RuntimeError("Failed to get token: Unauthorized (401)")

            self.token = data["message"]["body"]["user_token"]
        elif self.token is None:
            if force:
                raise RuntimeError("Token rate-limited or unauthorized")
            raise RuntimeError("Failed to get token after max retries")

    @staticmethod
    def format_time(seconds: float) -> str:
        """Formats time in seconds to mm:ss.xx (hundredths)."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        hundredths = int((seconds % 1) * 100)
        return f"{minutes:02d}:{secs:02d}.{hundredths:02d}"

    def get_lrc_word_by_word(self, track_id: int) -> Optional[str]:
        """Fetches and parses RichSync word-by-word synced lyrics into LRC string."""
        data = self._get("track.richsync.get", {"track_id": str(track_id)})
        header = data.get("message", {}).get("header", {})

        if header.get("status_code") != 200:
            return None

        raw_richsync_body = data["message"]["body"]["richsync"]["richsync_body"]
        richsync_body = json.loads(raw_richsync_body)

        lrc_lines = []

        for item in richsync_body:
            line_start_ts = item["ts"]
            line_end_te = item["te"]
            
            line_str = f"[{self.format_time(line_start_ts)}] "

            for word_info in item.get("l", []):
                word_offset = word_info["o"]
                word_text = word_info["c"]
                word_absolute_time = self.format_time(line_start_ts + word_offset)
                
                line_str += f"<{word_absolute_time}> {word_text} "

            line_str += f"<{self.format_time(line_end_te)}>"
            lrc_lines.append(line_str)

        return "\n".join(lrc_lines)

    def get_word_by_word_lyrics(self, artist: str, track: str, album: Optional[str] = None) -> Optional[str]:
        """Main method to search track and return word-by-word lyrics."""
        # 1. Ensure token exists
        if not self.token:
            self.get_token()

        # 2. Search for the track
        query = {
            "q_track": track,
            "q_artist": artist,
            "page_size": "1",
            "page": "1",
        }
        if album:
            query["album"] = album

        search_data = self._get("matcher.track.get", query)
        header = search_data.get("message", {}).get("header", {})

        if header.get("status_code") == 401:
            self.token = None
            return None

        if header.get("status_code") != 200:
            return None

        track_data = search_data["message"]["body"]["track"]
        track_id = track_data["track_id"]
        has_rich_sync = track_data.get("has_richsync", 0)

        # 3. If word-by-word lyrics exist, fetch them
        if has_rich_sync:
            return self.get_lrc_word_by_word(track_id)
        else:
            print(f"Track found (ID: {track_id}), but RichSync word-by-word lyrics are not available for this track.")
            return None


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    mx = Musixmatch()
    
    track = "Alors on Danse (Radio Edit)"
    artist = "Stromae"
    
    print(f"Searching lyrics for '{track}' by '{artist}'...")
    lyrics = mx.get_word_by_word_lyrics(artist=artist, track=track)

    if lyrics:
        # Define filename (e.g., "Coldplay - Viva La Vida.lrc")
        filename = f"{artist} - {track}.lrc"
        
        # Write to file in the current directory
        with open(filename, "w", encoding="utf-8") as f:
            f.write(lyrics)
            
        print(f"\nSaved successfully to: {filename}")
    else:
        print("Could not retrieve word-by-word lyrics.")