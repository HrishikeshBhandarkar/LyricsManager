import time
import json
import requests
from pathlib import Path


# MY TOKEN CACHE PATH:
# Path.home() returns the absolute path to the current user's home directory across operating systems:
# - On Windows: C:\Users\hrish
# - On Linux/Mac: /home/hrish
# The '/' operator is overloaded by Python's pathlib.Path class to safely construct subpaths.
# I save the Musixmatch user token in ~/.musixmatch_token.txt so it persists across CLI app restarts.
# This prevents my app from requesting a new token on every single song run, which would trigger IP rate-limiting!
TOKEN_CACHE_FILE = Path.home() / ".musixmatch_token.txt"


class Musixmatch:
    """
    MY MUSIXMATCH API CLIENT:
    Connects directly to Musixmatch's official desktop application REST API (apic-desktop.musixmatch.com).
    Handles user authentication tokens, disk token caching, HTTP rate-limit handling,
    and parses Musixmatch RichSync JSON payloads into word-by-word ELRC formatted strings.
    """
    # The base URL endpoint for Musixmatch's desktop app web service API version 1.1
    ROOT_URL = "https://apic-desktop.musixmatch.com/ws/1.1/"

    def __init__(self):
        # requests.Session() creates a persistent HTTP session object.
        # It enables HTTP Keep-Alive, reusing underlying TCP socket connections for faster network calls.
        self.session = requests.Session()
        
        # Musixmatch API endpoints enforce strict client validation.
        # If standard Python-requests User-Agents are sent, Musixmatch returns HTTP 401 or 403 errors.
        # I update self.session.headers with browser & desktop app headers to emulate authentic requests:
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.musixmatch.com",
            "Referer": "https://www.musixmatch.com/",
        })
        self.token = None

    def _get(self, action: str, params: dict) -> dict:
        """
        MY INTERNAL GET HELPER METHOD:
        - action: API endpoint action string (e.g. 'token.get', 'matcher.track.get', 'track.richsync.get')
        - params: dictionary of query parameters specific to the request call
        Automates adding required desktop app parameters (app_id, usertoken, timestamp) to every request.
        """
        # Musixmatch desktop client app identifier string required by API
        params["app_id"] = "web-desktop-app-v1.0"
        
        # Attach user token to request query parameters if token exists and request is not token initialization
        if self.token and action != "token.get":
            params["usertoken"] = self.token
            
        # Musixmatch API requires a cache-busting timestamp parameter 't' in milliseconds.
        # time.time() returns current time in floating seconds since UNIX epoch.
        # Multiplying by 1000 and casting to int converts seconds to 13-digit millisecond integer string.
        params["t"] = str(int(time.time() * 1000))
        
        # Construct full target URL string by appending action endpoint to base root URL
        url = self.ROOT_URL + action
        
        # Sest using sessend HTTP GET requion object with a 10-second connection timeout
        response = self.session.get(url, params=params, allow_redirects=True, timeout=10)
        
        # raise_for_status() checks HTTP status code; raises an HTTPError exception if code is 4xx or 5xx
        response.raise_for_status() # NOTE its best to put this inside a try and except block
        
        # .json() parses HTTP response body bytes from JSON string into Python dictionary/list
        return response.json()

    def get_token(self, force: bool = False) -> None:
        """
        MY TOKEN MANAGEMENT & DISK CACHING LOGIC:
        - force: if True, ignores cached token on disk and forces API to generate a fresh token.
        Saves user token in ~/.musixmatch_token.txt so it survives script re-runs across CLI commands.
        """
        # Check if force is False and token cache file exists on local hard drive
        if not force and TOKEN_CACHE_FILE.exists():
            try:
                # TOKEN_CACHE_FILE.read_text() opens file, reads contents as string, and closes file.
                # .strip() removes leading/trailing whitespace and newline characters.
                cached_token = TOKEN_CACHE_FILE.read_text().strip()
                if cached_token:
                    self.token = cached_token
                    return  # Successfully loaded token from disk; return early!
            except Exception:
                pass  # If disk read fails, fall through to fetch token from web API

        # If no saved token on disk, call Musixmatch token.get API endpoint
        try:
            data = self._get("token.get", {"user_language": "en"})
            
            # Musixmatch wraps API status inside JSON payload structure: data["message"]["header"]["status_code"]
            status_code = data.get("message", {}).get("header", {}).get("status_code")
            if status_code == 200:
                # Extract user token string from nested JSON body dictionary
                user_token = data["message"]["body"]["user_token"]
                self.token = user_token
                
                # TOKEN_CACHE_FILE.write_text() creates or overwrites disk file with token string
                TOKEN_CACHE_FILE.write_text(user_token)
        except Exception:
            self.token = None

    @staticmethod
    def format_time(seconds: float) -> str:
        """
        MY TIME FORMATTER UTILITY:
        Converts floating point seconds (e.g. 76.5432) into standard LRC timestamp string format 'MM:SS.xx'.
        - seconds // 60: integer floor division calculates total whole minutes.
        - seconds % 60: modulus operator calculates remaining whole seconds (0 to 59).
        - (seconds % 1) * 100: gets decimal fractional remainder and scales it to 2-digit hundredths.
        - f"{minutes:02d}:{secs:02d}.{hundredths:02d}": f-string format specifier ':02d' zero-pads integers to width of 2.
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        hundredths = int((seconds % 1) * 100)
        return f"{minutes:02d}:{secs:02d}.{hundredths:02d}"

    def get_word_by_word_lyrics(self, artist: str, track: str) -> str:
        """
        MY MUSIXMATCH RICHSYNC PARSER ENGINE:
        1. Calls 'matcher.track.get' with song title & artist to search Musixmatch catalog.
        2. Retrieves 'track_id' and checks flag 'has_richsync' (1 if word-by-word synced lyrics exist).
        3. Calls 'track.richsync.get' to retrieve raw RichSync JSON array.
        4. Parses RichSync array where each item contains:
           - 'ts': line start timestamp in seconds (float)
           - 'te': line end timestamp in seconds (float)
           - 'l': list of word dicts containing 'o' (offset seconds from line start) and 'c' (word text string).
        5. Computes absolute word timestamp = line_start_ts + word_offset and constructs ELRC format string.
        """
        if not self.token:
            self.get_token()
        if not self.token:
            return ""

        # Build search query parameter dictionary
        query = {"q_track": track, "q_artist": artist, "page_size": "1", "page": "1"}
        search_data = self._get("matcher.track.get", query)
        header = search_data.get("message", {}).get("header", {})

        # MY RE-AUTHENTICATION RETRY LOGIC:
        # If stored token has expired on server, API returns status 401 (Unauthorized).
        # In this case, I delete (~/.musixmatch_token.txt), reset self.token, force fetch a new token, and retry search once!
        if header.get("status_code") == 401:
            TOKEN_CACHE_FILE.unlink(missing_ok=True)  # unlink() deletes the file from hard drive
            self.token = None
            self.get_token(force=True)  # Force request fresh token
            if not self.token:
                return ""
            search_data = self._get("matcher.track.get", query)
            header = search_data.get("message", {}).get("header", {})

        if header.get("status_code") != 200:
            return ""

        # Safely extract track dictionary from nested JSON structure using chained .get() calls
        track_data = search_data.get("message", {}).get("body", {}).get("track", {})
        track_id = track_data.get("track_id")
        has_rich_sync = track_data.get("has_richsync", 0)

        # Check if Musixmatch confirms RichSync word-by-word lyrics are present for this song
        if has_rich_sync and track_id:
            data = self._get("track.richsync.get", {"track_id": str(track_id)})
            raw_richsync_body = data.get("message", {}).get("body", {}).get("richsync", {}).get("richsync_body")
            if not raw_richsync_body:
                return ""

            # raw_richsync_body is returned as an escaped JSON string inside JSON; json.loads() parses string into Python list
            richsync_body = json.loads(raw_richsync_body)
            lrc_lines = []
            
            # Iterate through each line dictionary in richsync_body list
            for item in richsync_body:
                line_start_ts = item["ts"]  # Floating point line start time in seconds
                line_end_te = item["te"]    # Floating point line end time in seconds
                
                # Start line string with line header timestamp tag [MM:SS.xx]
                line_str = f"[{self.format_time(line_start_ts)}] "
                
                # Iterate over word offset list 'l'
                # Each word dict contains 'o' (word start offset relative to line ts) and 'c' (word text string)
                for word_info in item.get("l", []):
                    word_offset = word_info["o"]  # Offset in seconds from line start
                    word_text = word_info["c"]    # Word text string (e.g. "Lock")
                    
                    # MY ABSOLUTE TIME CALCULATION:
                    # Line timestamp + relative word offset = absolute word timestamp in song timeline!
                    word_absolute_time = self.format_time(line_start_ts + word_offset)
                    line_str += f"<{word_absolute_time}> {word_text} "
                
                # MY LINE END TIMESTAMP:
                # Append line end timestamp <MM:SS.xx> at end of line to tell player when line finishes!
                line_str += f"<{self.format_time(line_end_te)}>"
                lrc_lines.append(line_str)
                
            # '\n'.join(lrc_lines) combines list of line strings into single multi-line string separated by newlines
            return "\n".join(lrc_lines)
        return ""

    def get_line_lyrics(self, artist: str, track: str) -> str:
        """
        MY MUSIXMATCH LINE SUBTITLES PARSER:
        Calls 'track.subtitles.get' with subtitle_format='lrc' to retrieve standard line-synced lyrics.
        """
        if not self.token:
            self.get_token()
        if not self.token:
            return ""

        query = {"q_track": track, "q_artist": artist, "page_size": "1", "page": "1"}
        search_data = self._get("matcher.track.get", query)
        header = search_data.get("message", {}).get("header", {})

        if header.get("status_code") == 401:
            TOKEN_CACHE_FILE.unlink(missing_ok=True)
            self.token = None
            self.get_token(force=True)
            if not self.token:
                return ""
            search_data = self._get("matcher.track.get", query)
            header = search_data.get("message", {}).get("header", {})

        if header.get("status_code") != 200:
            return ""

        track_data = search_data.get("message", {}).get("body", {}).get("track", {})
        track_id = track_data.get("track_id")
        has_subtitles = track_data.get("has_subtitles", 0)

        if has_subtitles and track_id:
            sub_data = self._get("track.subtitles.get", {"track_id": str(track_id), "subtitle_format": "lrc"})
            subtitle_body = sub_data.get("message", {}).get("body", {}).get("subtitle", {}).get("subtitle_body")
            if subtitle_body:
                return subtitle_body
        return ""


# Instantiate global Musixmatch client to reuse TCP session and cached authentication token
mx_client = Musixmatch()


def musixmatch_provider(data: dict, type: str = "enhanced") -> str:
    """
    MY MUSIXMATCH PROVIDER ROUTER:
    Calls my Musixmatch client methods based on user mode.
    If enhanced requested, tries get_word_by_word_lyrics() (RichSync) first, 
    and falls back to get_line_lyrics() if RichSync is unavailable.
    """
    try:
        if type.lower() in ("enhanced", "word"):
            lyrics = mx_client.get_word_by_word_lyrics(artist=data["artist"], track=data["title"])
            if not lyrics:
                lyrics = mx_client.get_line_lyrics(artist=data["artist"], track=data["title"])
            return lyrics
        else:
            return mx_client.get_line_lyrics(artist=data["artist"], track=data["title"])
    except Exception:
        return ""
