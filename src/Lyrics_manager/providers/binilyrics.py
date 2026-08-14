import re
import requests
import xml.etree.ElementTree as ET

from .utils import ms_to_lrc_time


# =====================================================================
# MY TTML PARSER ENGINE (FOR BINILYRICS & APPLE MUSIC TTML XML)
# =====================================================================
def parse_ttml(xml_text: str, is_enhanced: bool = True) -> str:
    """
    MY TTML TO LRC/ELRC CONVERTER ENGINE:
    - What is TTML? Timed Text Markup Language (TTML) is an XML format used by Apple Music & BiniLyrics.
    - How my parser works:
      1. Namespace Agnostic Parsing: TTML XML tags contain varying xmlns namespace prefixes 
         (e.g., '{http://www.w3.org/ns/ttml}p' vs '{http://www.w3.org/2006/10/ttaf1}p').
         I strip namespaces using elem.tag.split("}")[-1] so my code parses ANY TTML document correctly!
      2. Vocal Role Detection: Inspects attributes (agent, role, class, voice) to format singer roles:
         - Background vocals -> [bg:MM:SS.xx]
         - Voice 1 (Main singer) -> [MM:SS.xx]v1
         - Voice 2 (Duet singer) -> [MM:SS.xx]v2
      3. Word & Line Timestamps: Extracts line start, word start <MM:SS.xx>, and line ending <MM:SS.xx> timestamps.
    """
    def convert_time(ttml_time: str, is_line_header: bool = True, role: str = "") -> str:
        """
        MY TTML TIMESTAMP CONVERTER HELPER:
        Converts TTML XML timestamp strings into formatted LRC/ELRC timestamp tags.
        Handles three different TTML time formats:
        1. 'HH:MM:SS.ms' (3 parts split by ':') -> e.g. "00:01:23.450"
        2. 'MM:SS.ms' (2 parts split by ':')    -> e.g. "01:23.45"
        3. 'SS.ms' / 'SSs' (1 part)             -> e.g. "76.54s" or "76.54"
        """
        if not ttml_time:
            return ""
            
        # .strip() removes whitespace; .rstrip("s") removes trailing 's' unit character if time is "76.54s"
        ttml_time = ttml_time.strip().rstrip("s")
        parts = ttml_time.split(":")
        
        # Case 1: HH:MM:SS.xx (Hours:Minutes:Seconds)
        if len(parts) == 3:
            # int(parts[0]) * 60 converts hours to minutes, then adds int(parts[1]) minutes
            total_minutes = int(parts[0]) * 60 + int(parts[1])
            seconds_part = parts[2]  # "SS.xx" string
            
        # Case 2: MM:SS.xx (Minutes:Seconds)
        elif len(parts) == 2:
            total_minutes = int(parts[0])  # "MM" string
            seconds_part = parts[1]        # "SS.xx" string
            
        # Case 3: Raw seconds "SS.xx" or "76.54"
        elif len(parts) == 1:
            try:
                total_seconds = float(parts[0])
                total_minutes = int(total_seconds // 60)  # Integer floor division gets total whole minutes
                seconds_part = f"{total_seconds % 60:.2f}"  # Modulus gets remaining seconds rounded to 2 decimals
            except ValueError:
                return ""
        else:
            return ""

        # Split seconds string "SS.hundredths" by '.' to isolate whole seconds from fractional milliseconds
        sec_parts = seconds_part.split(".")
        try:
            secs = int(sec_parts[0])  # Whole seconds integer
        except ValueError:
            return ""
            
        # MY MILLISECONDS PADDING & TRUNCATION LOGIC:
        # sec_parts[1] gets fractional part string (e.g. "5", "54", "543").
        # .ljust(2, "0") left-justifies string padding with '0' if single digit ("5" -> "50").
        # [:2] truncates string to maximum of 2 digits if 3 digits ("543" -> "54").
        millis_raw = sec_parts[1] if len(sec_parts) > 1 else "00"
        hundredths = millis_raw.ljust(2, "0")[:2]

        time_str = f"{total_minutes:02d}:{secs:02d}.{hundredths}"

        # MY VOCAL ROLE HEADER FORMATTER:
        # If formatting a line header timestamp [MM:SS.xx]:
        # - role == 'bg': formats as [bg:MM:SS.xx]
        # - role == 'v2': formats as [MM:SS.xx]v2
        # - role == 'v1': formats as [MM:SS.xx]v1
        # - default    : formats as [MM:SS.xx]
        # If formatting a word or line-end timestamp (is_line_header=False):
        # - formats as <MM:SS.xx>
        if is_line_header:
            if role == "bg":
                return f"[bg:{time_str}]"
            elif role == "v2":
                return f"[{time_str}]v2"
            elif role == "v1":
                return f"[{time_str}]v1"
            else:
                return f"[{time_str}]"
        else:
            return f"<{time_str}>"

    def get_vocal_role(elem) -> str:
        """
        MY VOCAL ROLE DETECTOR HELPER:
        Iterates over element XML attributes to detect singer roles (v1, v2, bg).
        - elem.attrib.items(): returns (attribute_key, attribute_value) tuples.
        - k.lower().split("}")[-1]: removes XML namespace prefix from attribute key 
          (e.g., '{http://www.w3.org/ns/ttml#metadata}agent' -> 'agent').
        """
        for k, v in elem.attrib.items():
            key_lower = k.lower().split("}")[-1]  # Key string (agent, role, class, voice)
            val_lower = str(v).lower().strip()    # Value string (bg, v1, v2, etc.)
            
            if key_lower in ("agent", "role", "class", "voice"):
                # Check for background vocal tags
                if any(x in val_lower for x in ("bg", "background", "x-bg")):
                    return "bg"
                # Check for second singer / duet vocal tags
                elif any(x in val_lower for x in ("v2", "voice2", "singer2")) or val_lower == "2":
                    return "v2"
                # Check for main singer vocal tags
                elif any(x in val_lower for x in ("v1", "voice1", "singer1")) or val_lower == "1":
                    return "v1"
        return ""

    try:
        # ET.fromstring(xml_text) parses raw XML string into an ElementTree root Element node object
        root = ET.fromstring(xml_text)
        lrc_lines = []

        # MY NAMESPACE-AGNOSTIC TREE ITERATOR:
        # root.iter() recursively traverses every single node in the entire XML tree document.
        # elem.tag returns full tag string like '{http://www.w3.org/ns/ttml}p'.
        # elem.tag.split("}")[-1] splits by '}' and takes last element [-1], leaving just 'p'!
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]  # Isolates clean XML tag name ('p', 'span', 'head', etc.)
            
            if tag == "p":  # In TTML XML, <p> elements represent paragraph lyric lines
                line_begin = ""
                line_end = ""
                
                # Iterate over line <p> element attributes to extract 'begin' and 'end' timestamps
                for k, v in elem.attrib.items():
                    if k == "begin" or k.endswith("}begin"):
                        line_begin = v
                    elif k == "end" or k.endswith("}end"):
                        line_end = v

                # Detect vocal role (bg, v1, v2) for this line
                line_role = get_vocal_role(elem)
                
                # Convert line start timestamp into line header tag string
                line_header = convert_time(line_begin, is_line_header=True, role=line_role) if line_begin else ("[bg:00:00.00]" if line_role == "bg" else ("[00:00.00]v2" if line_role == "v2" else ("[00:00.00]v1" if line_role == "v1" else "[00:00.00]")))
                
                # Convert line end timestamp into ending tag string <MM:SS.xx>
                line_end_tag = convert_time(line_end, is_line_header=False) if line_end else ""

                if is_enhanced:
                    words_in_line = []
                    
                    # elem.iter() traverses all child nodes under current line <p> element
                    for child in elem.iter():
                        child_tag = child.tag.split("}")[-1]
                        if child_tag == "span":  # In TTML XML, <span> elements represent individual words
                            word_text = child.text or ""  # Extract word text string inside <span> tag
                            word_begin = ""
                            
                            # Extract word start timestamp from <span> attributes
                            for k, v in child.attrib.items():
                                if k == "begin" or k.endswith("}begin"):
                                    word_begin = v
                                    break

                            if not word_text.strip():
                                continue  # Skip empty whitespace spans

                            if word_begin:
                                # Convert word start timestamp into <MM:SS.xx> tag string
                                word_time = convert_time(word_begin, is_line_header=False)
                                words_in_line.append(f"{word_time}{word_text}")
                            else:
                                words_in_line.append(word_text)

                    # MY ENHANCED LINE ASSEMBLY LOGIC:
                    if words_in_line:
                        # Join line header tag with space-separated word timestamp tags
                        full_line = f"{line_header}" + " ".join(words_in_line)
                        if line_end_tag:
                            # Append line end timestamp at the very end of line!
                            full_line += f" {line_end_tag}"
                        lrc_lines.append(full_line)
                    else:
                        # Fallback if line has no <span> tags: extract all inner text using "".join(elem.itertext())
                        full_text = "".join(elem.itertext()).strip()
                        if full_text:
                            full_line = f"{line_header}{full_text}"
                            if line_end_tag:
                                full_line += f" {line_end_tag}"
                            lrc_lines.append(full_line)
                else:
                    # Standard line mode requested: extract plain line text without word timestamp tags
                    full_text = "".join(elem.itertext()).strip()
                    if full_text:
                        lrc_lines.append(f"{line_header}{full_text}")

        # Combine all processed lines into single multi-line string
        return "\n".join(lrc_lines)
    except Exception:
        return ""


def biniLy(data: dict, type: str = "enhanced") -> str:
    """
    MY BINILYRICS PROVIDER:
    1. Queries BiniLyrics API endpoint (https://lyrics-api.binimum.org/getLyrics?q=title+artist).
    2. Searches returned 'results' array for entries matching timing_type == 'word'.
    3. Fetches raw TTML XML file content from lyricsUrl.
    4. Passes raw XML to my parse_ttml converter engine to generate ELRC formatted lyrics.
    """
    baseUrl = "https://lyrics-api.binimum.org/getLyrics"
    params = {"q": f"{data['title']} {data['artist']}"}
    lyricsUrl = None

    try:
        response = requests.get(baseUrl, params=params, timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            if json_data is not None:
                results = json_data.get("results", [])
                # Iterate over search results list to locate word-by-word TTML entry
                for o in results:
                    if o.get("timing_type") == "word":
                        lyricsUrl = o.get("lyricsUrl")
                        break  # Found word-by-word lyrics URL; stop loop!

        if lyricsUrl:
            is_enhanced_flag = (type.lower() in ("enhanced", "word"))
            # Fetch raw TTML XML text from storage URL
            fileTTML = requests.get(lyricsUrl, timeout=5)
            # Parse TTML XML into ELRC string format
            s_lyrics = parse_ttml(fileTTML.text, is_enhanced=is_enhanced_flag)
            return s_lyrics
    except Exception:
        return ""

    return ""
