import requests


class MusixmatchService:

    def __init__(self):
        self.base_url = "https://apic-desktop.musixmatch.com/ws/1.1"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        self.token = None

    def get_token(self) -> str:
        """Step 1: Fetches an anonymous user token required by Musixmatch API."""
        url = f"{self.base_url}/token.get"
        params = {"app_id": "web-desktop-app-v1.0"}

        try:
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                # Check API status inside payload
                if data.get("message", {}).get("header", {}).get("status_code") == 200:
                    self.token = (
                        data["message"]["body"].get("user_token")
                    )
                    print(f"[✔] Acquired Musixmatch Token: {self.token}")
                    return self.token
            print("Failed to acquire Musixmatch token.")
            return None
        except Exception as e:
            print(f"Error fetching token: {e}")
            return None

    def get_rich_synced_lyrics(
        self, title: str, artist: str, album: str = None
    ):
        """Step 2 & 3: Requests rich-synced (word-by-word) lyrics for a track."""
        # Ensure we have a valid token before making the request
        if not self.token:
            self.get_token()

        if not self.token:
            print("Cannot proceed without a valid token.")
            return None

        # Search for track / fetch lyrics endpoint
        url = f"{self.base_url}/macro.subtitles.get"
        params = {
            "format": "json",
            "namespace": "lyrics_synchro",
            "q_track": title,
            "q_artist": artist,
            "usertoken": self.token,
            "app_id": "web-desktop-app-v1.0",
        }

        if album:
            params["q_album"] = album

        try:
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                body = data.get("message", {}).get("body", {})

                # Extract rich sync structure (word-by-word data)
                macro_calls = body.get("macro_calls", {})
                richsync_data = (
                    macro_calls.get("track.richsync.get", {})
                    .get("message", {})
                    .get("body", {})
                    .get("richsync", {})
                )

                if richsync_data:
                    return richsync_data.get("rich_sync_body")
                else:
                    print(
                        "No rich-synced (word-level) lyrics found for this track."
                    )
                    return None

        except Exception as e:
            print(f"Error fetching Musixmatch lyrics: {e}")
            return None


if __name__ == "__main__":
    mxm = MusixmatchService()

    # Get token and request lyrics
    title = "Open Hearts"
    artist = "The Weeknd"

    rich_lyrics = mxm.get_rich_synced_lyrics(title, artist)

    if rich_lyrics:
        print("\n--- Raw RichSync Output Preview ---")
        print(str(rich_lyrics)[:500])