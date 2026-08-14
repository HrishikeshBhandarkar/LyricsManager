# MY SYNCEDLYRICS SAFE IMPORT CHECK:
# In VS Code, 'import syncedlyrics' shows a red underline if the active interpreter environment
# has not indexed the library. Using try-except ImportError ensures my code NEVER crashes if missing!
try:
    import syncedlyrics
    SYNCEDLYRICS_AVAILABLE = True
except ImportError:
    SYNCEDLYRICS_AVAILABLE = False


def syncedlyrics_provider(data: dict) -> str:
    """
    MY SYNCEDLYRICS PROVIDER:
    Uses the 'syncedlyrics' Python package to search external services (NetEase, Megalobiz, Deezer).
    Safe against missing package errors via SYNCEDLYRICS_AVAILABLE flag.
    """
    if not SYNCEDLYRICS_AVAILABLE:
        return ""
    try:
        search_term = f"{data['title']} {data['artist']}"
        lrc_res = syncedlyrics.search(search_term)
        return lrc_res if lrc_res else ""
    except Exception:
        return ""
