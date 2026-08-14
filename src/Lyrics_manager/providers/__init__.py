"""
MY PROVIDERS PACKAGE:
Each provider module handles searching, fetching, decrypting, and parsing lyrics from a specific API source.
"""
from .utils import ms_to_lrc_time, ms_to_lrc_time_3, is_truly_enhanced
from .lrclib import lrclib
from .binilyrics import biniLy, parse_ttml
from .musixmatch import musixmatch_provider, mx_client
from .syncedlyrics_prov import syncedlyrics_provider
from .paxsenix import paxsenix
from .kugou import kugou_provider, decode_krc, parse_krc_to_elrc
from .netease import netease_provider, parse_yrc_to_elrc
from .qqmusic import qqmusic_provider, parse_qrc_to_elrc

__all__ = [
    "ms_to_lrc_time", "ms_to_lrc_time_3", "is_truly_enhanced",
    "lrclib",
    "biniLy", "parse_ttml",
    "musixmatch_provider", "mx_client",
    "syncedlyrics_provider",
    "paxsenix",
    "kugou_provider", "decode_krc", "parse_krc_to_elrc",
    "netease_provider", "parse_yrc_to_elrc",
    "qqmusic_provider", "parse_qrc_to_elrc",
]
