import requests
from .utils import ms_to_lrc_time, is_truly_enhanced


# PAXSENIX APPLE MUSIC HEADERS
PAXSENIX_HEADERS = {"User-Agent": "Metrolist/Unknown", "Accept": "application/json"}


def paxsenix(data: dict) -> str:
    """
    MY PAXSENIX PROVIDER:
    1. Queries iTunes Search API (https://itunes.apple.com/search) to resolve song title & artist 
       into an official Apple Music trackId integer string.
    2. Queries Paxsenix Apple Music Lyrics API (https://lyrics.paxsenix.org/apple-music/lyrics?id=trackId).
    3. Builds ELRC strings and validates word timestamp variations using my is_truly_enhanced validator.
    """
    title = data["title"]
    artist = data["artist"]
    try:
        # requests.utils.quote() encodes special characters and spaces into URL percent-encoding (e.g. ' ' -> '%20')
        query = requests.utils.quote(f"{title} {artist}")
        itunes_url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        res_itunes = requests.get(itunes_url, timeout=5)
        
        if res_itunes.status_code != 200 or not res_itunes.json().get("results"):
            return ""
            
        # Extract Apple Music trackId integer as string
        track_id = str(res_itunes.json()["results"][0]["trackId"])
        pax_url = "https://lyrics.paxsenix.org/apple-music/lyrics"
        res_pax = requests.get(pax_url, params={"id": track_id}, headers=PAXSENIX_HEADERS, timeout=8)
        
        if res_pax.status_code == 200:
            pax_data = res_pax.json()
            elrc_data = pax_data.get("elrc")
            if elrc_data and is_truly_enhanced(elrc_data):
                return elrc_data

            content = pax_data.get("content", [])
            if not content:
                return ""

            elrc_lines = []
            for line in content:
                line_time = ms_to_lrc_time(line.get("timestamp", 0))
                elrc_line = f"[{line_time}] "
                word_list = line.get("text", [])
                if isinstance(word_list, list):
                    for word in word_list:
                        if isinstance(word, dict):
                            word_time = ms_to_lrc_time(word.get("timestamp", 0))
                            word_str = word.get("text", "")
                            elrc_line += f"<{word_time}>{word_str} "
                        elif isinstance(word, str):
                            elrc_line += f"{word} "
                elrc_lines.append(elrc_line.strip())

            final_text = "\n".join(elrc_lines)
            if is_truly_enhanced(final_text):
                return final_text
    except Exception:
        return ""
    return ""
