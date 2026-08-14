import requests
import json
import re
import xml.etree.ElementTree as ET

def get_song_mid(song_name, artist_name=""):
    """
    Search for a song on QQ Music and return its unique songmid.
    """
    search_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    params = {
        "p": 1,
        "n": 1,
        "w": f"{song_name} {artist_name}".strip(),
        "format": "json"
    }
    headers = {
        "Referer": "https://y.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()
    
    try:
        song_list = data["data"]["song"]["list"]
        if song_list:
            top_result = song_list[0]
            print(f"Found: '{top_result['songname']}' by {top_result['singer'][0]['name']}")
            return top_result["songmid"]
    except KeyError:
        pass
        
    return None

def fetch_qrc_lyrics(song_mid):
    """
    Fetch raw word-by-word QRC lyrics payload from QQ Music API.
    """
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
    params = {
        "songmid": song_mid,
        "g_tk": "5381",
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf-8",
        "nobase64": "1",  # Request raw text where supported
        "qrc": "1"        # Request word-by-word QRC timing format
    }
    headers = {
        "Referer": "https://y.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    # Try fetching QRC first, fallback to standard lyric string
    qrc_text = data.get("qrc") or data.get("lyric")
    return qrc_text

def parse_qrc(qrc_text):
    """
    Parses QRC string containing line and word-level timestamps into a structured list.
    """
    if not qrc_text:
        return []

    # If the response is wrapped in XML tags (<Qrc>...</Qrc>), extract inner text
    if qrc_text.startswith("<?xml") or "<Qrc" in qrc_text:
        try:
            root = ET.fromstring(qrc_text)
            qrc_text = root.find(".//Lyric_1").attrib.get("LyricContent", qrc_text)
        except Exception:
            pass

    parsed_lines = []
    
    # Matches line format: [line_start_ms, line_duration_ms] line_content
    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*)")
    # Matches word format: word_text(word_start_ms, word_duration_ms)
    word_pattern = re.compile(r"([^(]+)\((\d+),(\d+)\)")

    for line in qrc_text.splitlines():
        line_match = line_pattern.match(line)
        if line_match:
            line_start_ms, line_duration_ms, content = line_match.groups()
            
            words = []
            for word_match in word_pattern.finditer(content):
                word_text, word_start, word_dur = word_match.groups()
                words.append({
                    "word": word_text.strip(),
                    "start_ms": int(word_start),
                    "duration_ms": int(word_dur)
                })

            parsed_lines.append({
                "line_start_ms": int(line_start_ms),
                "line_duration_ms": int(line_duration_ms),
                "words": words
            })

    return parsed_lines

# --- Example Execution ---
if __name__ == "__main__":
    song_query = "Shape of You"
    artist_query = "Ed Sheeran"

    print(f"Searching for '{song_query}'...")
    mid = get_song_mid(song_query, artist_query)

    if mid:
        raw_qrc = fetch_qrc_lyrics(mid)
        word_synced_data = parse_qrc(raw_qrc)

        # Print top 3 lines with word timestamps as JSON
        print("\nParsed Word-by-Word Lyrics (First 3 lines):")
        print(json.dumps(word_synced_data[:3], indent=2, ensure_ascii=False))
    else:
        print("Song not found.")