import xml.etree.ElementTree as ET
from pathlib import Path
import requests


# Helper function to convert TTML timestamps (HH:MM:SS.mmm or MM:SS.mmm) into ELRC format ([MM:SS.xx] or <MM:SS.xx>)
def ttml_to_elrc_time(ttml_time: str, is_line_header: bool = False) -> str:
    if not ttml_time:
        return ""

    # Split the time string by colons
    parts = ttml_time.strip().split(":")

    # Calculate total minutes and extract seconds
    if len(parts) == 3:  # HH:MM:SS.mmm
        hours, minutes, seconds = parts
        total_minutes = int(hours) * 60 + int(minutes)
    elif len(parts) == 2:  # MM:SS.mmm
        minutes, seconds = parts
        total_minutes = int(minutes)
    else:
        return ""

    # Separate seconds and milliseconds/hundredths
    sec_parts = seconds.split(".")
    secs = int(sec_parts[0])
    hundredths = int(sec_parts[1][:2]) if len(sec_parts) > 1 else 0

    # Format as line header [mm:ss.xx] or word timestamp <mm:ss.xx>
    if is_line_header:
        return f"[{total_minutes:02d}:{secs:02d}.{hundredths:02d}]"
    else:
        return f"<{total_minutes:02d}:{secs:02d}.{hundredths:02d}>"


def fetch_bini(title: str, artist: str):
    baseUrl = "https://lyrics-api.binimum.org/getLyrics"
    params = {"q": f"{title} {artist}"}
    object = requests.get(baseUrl, params)

    lyricsUrl = None  # Initialize variable to prevent NameError if loop finds nothing

    if object.status_code == 200:
        data = object.json()
        print()
        if data != None:
            results = data.get("results", [])
            print(results)
            if results:
                for o in results:
                    if o.get("timing_type") == "word":
                        lyricsUrl = o.get("lyricsUrl")
                        break

            print(lyricsUrl)

    if not lyricsUrl:
        print("No word-level lyrics URL found.")
        return

    txt_path = (
        rf"C:\Users\hrish\Lyric_manager\Test\Response_API\BiniLyrics\{title}.txt"
    )
    data = requests.get(lyricsUrl)

    if data.status_code == 200:
        # Step 1: Save the raw TTML XML text file to disk
        with open(txt_path, "w", encoding="utf-8") as e:
            e.write(data.text)

        print(f"[✔] Saved raw XML to: {txt_path}")

        # =====================================================================
        # ADDED SECTION: PARSING THE XML & CONVERTING TO ELRC
        # =====================================================================

        # 1. Parse the XML string directly from 'data.text' using ElementTree
        root = ET.fromstring(data.text)

        # 2. Create an empty list to collect converted ELRC lines
        elrc_lines = []

        # 3. Find all paragraph tags (<p>) representing lyric lines in TTML XML
        for p in root.iter("{http://www.w3.org/ns/ttml}p"):

            # Extract line start timestamp and convert to line header format [mm:ss.xx]
            line_start_raw = p.attrib.get("begin", "00:00.00")
            line_header = ttml_to_elrc_time(line_start_raw, is_line_header=True)

            words_in_line = []

            # 4. Iterate over word span tags (<span>) inside this line
            for span in p.iter("{http://www.w3.org/ns/ttml}span"):
                word_text = span.text or ""
                word_begin_raw = span.attrib.get("begin")

                # Skip empty spaces or blank tags
                if not word_text.strip():
                    continue

                # If word has a timestamp, convert it to word tag <mm:ss.xx>
                if word_begin_raw:
                    word_time = ttml_to_elrc_time(
                        word_begin_raw, is_line_header=False
                    )
                    words_in_line.append(f"{word_time}{word_text}")
                else:
                    words_in_line.append(word_text)

            # 5. Join words together and append line header if words exist
            if words_in_line:
                full_elrc_line = f"{line_header} " + " ".join(words_in_line)
                elrc_lines.append(full_elrc_line)

        # 6. Combine all ELRC lines into a single string with newlines
        final_elrc_content = "\n".join(elrc_lines)

        # 7. Define path for saving .elrc file
        elrc_path = rf"C:\Users\hrish\Lyric_manager\Test\Response_API\BiniLyrics\{title}.elrc"

        # 8. Write converted content to the .elrc file on disk
        with open(elrc_path, "w", encoding="utf-8") as f:
            f.write(final_elrc_content)

        print(f"[✔] Converted & saved ELRC to: {elrc_path}\n")

        # 9. Print a small terminal preview of converted lines
        print("--- ELRC Preview ---")
        print("\n".join(elrc_lines[:5]))


if __name__ == "__main__":
    title = "Open Hearts"
    artist = "The Weeknd"
    fetch_bini(title, artist)