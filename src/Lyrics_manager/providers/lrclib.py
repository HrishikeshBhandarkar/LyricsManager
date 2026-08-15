import requests


def lrclib(data: dict) -> str:
    """
    MY LRCLIB PROVIDER:
    1. First attempts exact lookup via https://lrclib.net/api/get with track_name & artist_name.
    2. If artist is 'Unknown' or exact match returns 404, queries https://lrclib.net/api/search.
    Returns syncedLyrics if available, or falls back to plainLyrics.
    """
    title = data.get("title", "").strip()
    artist = data.get("artist", "").strip()
    
    if not title:
        return ""

    # Strategy 1: Exact lookup if artist is known
    if artist and artist.lower() not in ["unknown", "unknown artist", "none", ""]:
        get_url = "https://lrclib.net/api/get"
        params = {
            "track_name": title,
            "artist_name": artist
        }
        if "duration_ms" in data and data["duration_ms"]:
            params["duration"] = int(data["duration_ms"] / 1000)
            
        try:
            res = requests.get(get_url, params=params, timeout=5)
            if res.status_code == 200:
                rdata = res.json()
                lyrics = rdata.get("syncedLyrics") or rdata.get("plainLyrics")
                if lyrics:
                    return lyrics
        except Exception:
            pass

    # Strategy 2: Search endpoint fallback
    search_url = "https://lrclib.net/api/search"
    query = f"{title} {artist}".strip() if artist and artist.lower() not in ["unknown", "unknown artist"] else title
    
    try:
        res = requests.get(search_url, params={"q": query}, timeout=6)
        if res.status_code == 200:
            results = res.json()
            if isinstance(results, list) and results:
                # Prefer first result with syncedLyrics, else plainLyrics
                for item in results:
                    if item.get("syncedLyrics"):
                        return item["syncedLyrics"]
                for item in results:
                    if item.get("plainLyrics"):
                        return item["plainLyrics"]
    except Exception:
        pass

    return ""
