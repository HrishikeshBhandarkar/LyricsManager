import requests


def lrclib(data: dict) -> str:
    """
    MY LRCLIB PROVIDER:
    Queries the open-source LRCLIB REST API (https://lrclib.net/api/get) using track title & artist.
    Returns syncedLyrics if available, or falls back to plainLyrics.
    """
    baseUrl = "https://lrclib.net/api/get"
    params = {
        "track_name": data["title"],
        "artist_name": data["artist"]
    }
    try:
        response = requests.get(baseUrl, params=params, timeout=5)
        if response.status_code == 200:
            rdata = response.json()
            s_lyrics = rdata.get("syncedLyrics")
            if not s_lyrics:
                s_lyrics = rdata.get("plainLyrics")
            return s_lyrics
        else:
            return ""
    except Exception:
        return ""
