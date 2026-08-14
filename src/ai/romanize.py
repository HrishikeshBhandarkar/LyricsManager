"""
ROMANIZATION & TRANSLITERATION UTILITY
======================================
1. deromanize_hindi: Transliterates Hinglish (Latin) input into native Devanagari script.
2. romanize_universal: Converts any script (Devanagari, Kanji, Cyrillic) into ASCII/Latin
   phonetic representation using unidecode for DTW matching.
"""
import re
from unidecode import unidecode
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def deromanize_hindi(text: str) -> str:
    """
    Converts Hinglish (Latin alphabet) text into Devanagari script.
    If text is already in Devanagari script, returns it untouched.
    """
    if not text or not text.strip():
        return text

    # Check if text is already primarily Devanagari (range \u0900 - \u097F)
    devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
    latin_chars = len(re.findall(r'[a-zA-Z]', text))

    if devanagari_chars > latin_chars:
        return text  # Already in Devanagari script

    try:
        # Transliterate ITRANS / Hinglish -> Devanagari
        res = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        return res
    except Exception:
        return text


def romanize_display(text: str) -> str:
    """
    Converts native-script (e.g. Devanagari) text into romanized Latin (Hinglish)
    display text, preserving word spacing. Latin text is returned untouched.
    Ensures the transcript stays romanized for the model and in the ELRC output.
    """
    if not text or not text.strip():
        return text

    if not re.search(r'[\u0900-\u097F]', text):
        return text  # already romanized / Latin script

    try:
        res = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        if res.strip():
            return res
    except Exception:
        pass
    return unidecode(text)


def romanize_universal(text: str) -> str:
    """
    Converts any text string into a clean ASCII/Latin phonetic representation for DTW similarity.
    """
    if not text:
        return ""
    
    # 1. First attempt Indic transliteration if Devanagari
    if re.search(r'[\u0900-\u097F]', text):
        try:
            text = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
        except Exception:
            pass

    # 2. Universal unidecode fallback
    ascii_text = unidecode(text).lower()
    clean_ascii = re.sub(r'[^a-z0-9]', '', ascii_text)
    return clean_ascii
