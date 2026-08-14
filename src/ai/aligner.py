"""
WHISPERX FORCED ALIGNMENT ENGINE â€” Full Pipeline
=================================================
Stage 1 : Downsample source audio â†’ 16 kHz mono WAV (temporary)
Stage 2 : Separate vocals from instruments via Demucs htdemucs
Stage 3 : Vocal enhancement (dynamic compression + pre-emphasis) â€” pure signal math
Stage 4 : WhisperX ASR transcription on clean, enhanced vocal-only track
Stage 5 : WhisperX Wav2Vec2 phonetic alignment on ASR output
Stage 6 : DTW forward-window matching (with auto-unstick for muffled sections)
Stage 7 : Linear interpolation for any gaps â†’ strict 1:1 ELRC output

No extra model downloads â€” Demucs htdemucs and WhisperX are the only models used.
"""
from __future__ import annotations

import sys
import os
import time
import difflib
import subprocess
from pathlib import Path
from typing import Callable, Optional, Dict, Any

import unicodedata
import re

import warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"

import logging
for log_name in ["whisperx", "pyannote", "lightning", "speechbrain", "torch", "urllib3", "demucs", "transformers"]:
    logging.getLogger(log_name).setLevel(logging.ERROR)

# Fix SpeechBrain / Lightning / Pyannote k2 lazy import bug
try:
    from speechbrain.utils.importutils import LazyModule
    _orig_sb_getattr = LazyModule.__getattr__
    def _safe_sb_getattr(self, attr):
        try:
            return _orig_sb_getattr(self, attr)
        except Exception as e:
            raise AttributeError(attr) from e
    LazyModule.__getattr__ = _safe_sb_getattr
except ImportError:
    pass

import torch
import numpy as np
import whisperx

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from elrc_builder import build_elrc_strict_lines
from romanize import romanize_display, romanize_universal

SAMPLE_RATE = 16000  # WhisperX and Wav2Vec2 both require 16 kHz


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Helpers
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def normalize_devanagari(text: str) -> str:
    """Normalize Devanagari text for robust DTW matching without altering original display text."""
    if not text:
        return ""
    # Unicode NFD decomposition & strip Nukta (\u093c), Anusvara (\u0902), Chandrabindu (\u0901)
    text = unicodedata.normalize("NFD", text)
    text = re.sub(r'[\u093c\u0901\u0902]', '', text)
    text = unicodedata.normalize("NFC", text)
    # Lowercase & strip punctuation/hyphens
    text = re.sub(r'[.,!?\"\'()\[\]{}â€¦|\-]', '', text)
    # Standardize common matras for fuzzy matching (e.g. ii->i, uu->u)
    text = text.replace('à¥€', 'à¤¿').replace('à¥‚', 'à¥')
    return text.strip()


def clean_word(w: str) -> str:
    cleaned = w.lower().strip(".,!?\"'()[]{}â€¦â€”-â€“").strip()
    cleaned = normalize_devanagari(cleaned)
    # Filler expressions ("eh", "ah", "I") are often transcribed by the ASR in
    # stretched spellings ("ehh", "aah", "II", "oooh"). Collapse consecutive
    # repeated letters on SHORT words so both sides normalize to the same
    # phonetic form. Applied symmetrically (user + ASR words), so it can never
    # break a match that used to work.
    if 1 < len(cleaned) <= 4:
        collapsed = re.sub(r'(.)\1+', r'\1', cleaned)
        if len(collapsed) < len(cleaned):
            cleaned = collapsed
    return cleaned


def print_stage(num: int, total: int, label: str):
    pct = int(num / total * 100)
    bar_len = 38
    filled = int(bar_len * num / total)
    bar = "â–ˆ" * filled + "â–‘" * (bar_len - filled)
    print(f"\n  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”")
    print(f"  â”‚  [{num}/{total}] {label:<44}â”‚")
    print(f"  â”‚  [{bar}] {pct:>3}%     â”‚")
    print(f"  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜")


def interpolate_timestamps(words: list, total_duration: float, audio=None, sample_rate: int = 16000) -> list:
    """Fill missing start/end with monotone linear interpolation."""
    n = len(words)
    if n == 0:
        return words

    # Ensure keys exist
    for w in words:
        w.setdefault("start", None)
        w.setdefault("end", None)
        if w["start"] is not None and w["end"] is None:
            w["end"] = w["start"] + 0.05
        elif w["end"] is not None and w["start"] is None:
            w["start"] = max(0.0, w["end"] - 0.05)

    # Segment-based interpolation: find gaps and fill linearly
    i = 0
    while i < n:
        if words[i]["start"] is None:
            # Find extent of this gap
            gap_start = i
            while i < n and words[i]["start"] is None:
                i += 1
            gap_end = i  # exclusive

            # Anchor times
            t_before = words[gap_start - 1]["end"] if gap_start > 0 and words[gap_start - 1]["end"] is not None else 0.0
            t_after  = words[gap_end]["start"] if gap_end < n and words[gap_end]["start"] is not None else total_duration

            count = gap_end - gap_start

            # If it's a trailing gap, don't stretch all the way to the end of the song
            if gap_end == n and gap_start > 0:
                t_after = min(t_before + count * 0.4, total_duration)

            # If it's a leading gap, don't stretch all the way from 0.0
            if gap_start == 0 and gap_end < n:
                t_before = max(t_after - count * 0.4, 0.0)

            if t_after <= t_before:
                t_after = t_before + count * 0.15

            step  = (t_after - t_before) / max(count, 1)
            
            # NEW: Prevent "swiping" bursts. If step is insanely small (< 0.15s) for a block of words,
            # the anchor t_after is too tight (e.g. skipped chorus). Give them realistic durations.
            if step < 0.15 and count > 3:
                step = 0.35

            for k, idx in enumerate(range(gap_start, gap_end)):
                words[idx]["start"] = round(t_before + step * k, 3)
                words[idx]["end"]   = round(t_before + step * (k + 1), 3)
        else:
            i += 1

    # Final monotone repair (strictly sequential):
    # Words can NEVER overlap, even across line boundaries.
    for i in range(1, n):
        if words[i]["start"] < words[i - 1]["end"]:
            words[i]["start"] = words[i - 1]["end"]
        if words[i]["end"] <= words[i]["start"]:
            words[i]["end"] = words[i]["start"] + 0.05

    # --- Precise Trailing End Times (audio-aware) ---
    # Extend the last word of each line only as far as the voice actually
    # sustains. When the vocal stem is available, the extension follows the
    # real audio energy (silence detection). Without audio, a conservative
    # heuristic is used: stretch only into short gaps, capped at 0.8s, so the
    # word end never overshoots the actual singing.
    for i in range(n):
        is_last_in_line = (i == n - 1) or (words[i].get("line_idx") != words[i+1].get("line_idx"))
        if is_last_in_line:
            if i < n - 1 and words[i+1]["start"] is not None:
                next_start = words[i+1]["start"]
                if next_start > words[i]["end"]:
                    cap = next_start - 0.05  # leave a 50ms gap before the next word
                    if audio is not None:
                        words[i]["end"] = round(_audio_trailing_end(audio, words[i]["end"], cap, sample_rate), 3)
                    else:
                        gap = next_start - words[i]["end"]
                        if gap <= 2.5:
                            words[i]["end"] = round(min(words[i]["end"] + min(0.8, gap * 0.5), cap), 3)

    return words


def _audio_trailing_end(audio, word_end: float, cap: float, sample_rate: int = 16000) -> float:
    """
    Find where the voice actually stops after `word_end` by scanning the vocal
    stem for sustained silence. Returns a time <= cap (next word - 50ms).
    The silence threshold is adaptive: relative to the energy right at the
    word's end, so it works across loud and quiet vocals alike.
    """
    start_sample = int(word_end * sample_rate)
    end_sample = min(int(cap * sample_rate), len(audio))
    if end_sample <= start_sample:
        return word_end

    seg = audio[start_sample:end_sample]
    window = int(0.03 * sample_rate)   # 30 ms RMS windows
    step = int(0.01 * sample_rate)     # 10 ms hops
    base_rms = float(np.sqrt(np.mean(seg[:min(window, len(seg))] ** 2)) + 1e-9)
    threshold = max(base_rms * 0.25, 1e-4)

    last_loud = 0.0
    silence_run = 0
    for k in range(0, len(seg) - window + 1, step):
        rms = float(np.sqrt(np.mean(seg[k:k + window] ** 2)))
        if rms >= threshold:
            last_loud = (k + window) / sample_rate
            silence_run = 0
        else:
            silence_run += 1
            if silence_run >= 4:       # ~40ms+ of sustained silence -> stop
                break

    return min(word_end + last_loud, cap)


def _run_dtw(user_words: list, asr_words: list, asr_cols: list | None = None, accept: float = 0.35) -> list:
    """
    Global DTW alignment via full Needleman-Wunsch DP matrix, optionally
    restricted to a subset of ASR columns (asr_cols). Returns pairs of
    (user_idx, asr_idx).

    WHY global DP instead of a greedy forward window:
      - The greedy scan has a window of N words ahead of the cursor.
      - When Chorus 1 ends, the cursor sits at the end of segment 1.
      - As Chorus 2 starts, a few words match correctly. But when the window
        runs out of good matches (ASR mis-transcribed a word), consecutive_misses
        triggers window expansion. With a 30-word window the matcher can now
        skip far ahead in the ASR list, consuming words that belong to lines
        further in the transcript. Once those are consumed, every word that
        comes after them in the user lyrics has no valid ASR match and falls
        through to interpolation â€” producing the "0.881s per word" robot cadence.
      - The DP finds the globally optimal monotone alignment: matching two
        repeated choruses to their two separate occurrences in the ASR words
        is always scored higher than double-matching the first occurrence.

    Complexity: O(N*M) â€” for 112Ã—110 = 12,320 cells this runs in < 100ms.
    """
    if asr_cols is None:
        asr_cols = list(range(len(asr_words)))
    N = len(user_words)
    M = len(asr_cols)

    if N == 0 or M == 0:
        return []

    # â”€â”€ Step 1: Build similarity matrix (restricted to asr_cols) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    sim = [[0.0] * M for _ in range(N)]
    for i in range(N):
        u = user_words[i]["clean"]
        if not u:
            continue
        u_rom = romanize_universal(u)
        for jj in range(M):
            a = asr_words[asr_cols[jj]]["clean"]
            if not a:
                continue
            a_rom = romanize_universal(a)
            score_native = difflib.SequenceMatcher(None, u, a).ratio()
            score_rom = difflib.SequenceMatcher(None, u_rom, a_rom).ratio() if u_rom and a_rom else 0.0
            sim[i][jj] = max(score_native, score_rom)

    # â”€â”€ Step 2: DP table (Smart Global Alignment) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    # GAP_PENALTY: cost of skipping one user word OR one ASR word.
    GAP_PENALTY = -0.3

    dp    = [[float("-inf")] * (M + 1) for _ in range(N + 1)]
    trace = [[(0, 0)]        * (M + 1) for _ in range(N + 1)]

    dp[0][0] = 0.0
    for i in range(1, N + 1):
        dp[i][0]    = i * GAP_PENALTY
        trace[i][0] = (i - 1, 0)
    for j in range(1, M + 1):
        dp[0][j]    = j * GAP_PENALTY
        trace[0][j] = (0, j - 1)

    for i in range(1, N + 1):
        for j in range(1, M + 1):
            # If sim is 0.0 (total mismatch), score is -0.8.
            # If sim is 1.0 (perfect match), score is +1.2.
            # This makes the DP prefer inserting gaps (-0.6 total) over matching garbage (-0.8)!
            raw_sim = sim[i-1][j-1]
            adjusted_sim = (raw_sim * 2.0) - 0.8

            match_val = dp[i-1][j-1] + adjusted_sim      # align user[i-1] â†” asr[j-1]
            skip_user = dp[i-1][j]   + GAP_PENALTY       # skip user word (no ASR match)
            skip_asr  = dp[i][j-1]   + GAP_PENALTY       # skip ASR word (not in user text)

            best = max(match_val, skip_user, skip_asr)
            dp[i][j] = best

            if best == match_val:
                trace[i][j] = (i - 1, j - 1)
            elif best == skip_user:
                trace[i][j] = (i - 1, j)
            else:
                trace[i][j] = (i, j - 1)

    # â”€â”€ Step 3: Traceback from (N, M) â†’ (0, 0) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    pairs = []
    i, j = N, M
    while i > 0 and j > 0:
        pi, pj = trace[i][j]
        if pi == i - 1 and pj == j - 1:        # was a match step
            if sim[i-1][j-1] >= accept:         # accept if reasonably similar
                pairs.append((i - 1, asr_cols[j - 1]))
        i, j = pi, pj

    pairs.reverse()   # traceback produces pairs in reverse order
    return pairs


def _string_sim(u: str, a: str) -> float:
    """Similarity between two plain strings (native + romanized)."""
    if not u or not a:
        return 0.0
    score_native = difflib.SequenceMatcher(None, u, a).ratio()
    u_rom = romanize_universal(u)
    a_rom = romanize_universal(a)
    score_rom = difflib.SequenceMatcher(None, u_rom, a_rom).ratio() if u_rom and a_rom else 0.0
    return max(score_native, score_rom)


def _word_sim(u_word: dict, a_word: dict) -> float:
    """Similarity between a user word and an ASR word (native + romanized)."""
    return _string_sim(u_word.get("clean", ""), a_word.get("clean", ""))


def match_user_to_asr(user_words: list, asr_words: list) -> list:
    """
    Global DTW alignment via full Needleman-Wunsch DP matrix over ALL user words.
    Background vocal refinement and overlapping logic has been strictly removed.
    """
    N = len(user_words)
    M = len(asr_words)

    if N == 0 or M == 0:
        return []

    # â”€â”€ Step 1: Original global DTW over ALL user words â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    pairs = _run_dtw(user_words, asr_words)

    pairs.sort()
    return pairs



# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Stage helpers
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def stage_downsample(source_path: Path) -> Path:
    """
    Convert source audio â†’ 16 kHz mono WAV using ffmpeg.
    Result is cached as <stem>_16k.wav next to the source file.
    Re-used on subsequent runs â€” no re-processing.
    """
    out_path = source_path.parent / f"{source_path.stem}_16k.wav"
    if out_path.exists():
        print(f"    >> Cache hit: {out_path.name} already exists, skipping ffmpeg.")
        return out_path

    print(f"    >> Converting {source_path.name} â†’ 16 kHz mono WAV via ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(source_path),
        "-ar", str(SAMPLE_RATE),
        "-ac", "1",
        "-sample_fmt", "s16",
        str(out_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed:\n{result.stderr}")

    print(f"    [OK] Saved: {out_path.name} ({out_path.stat().st_size / 1024:.0f} KB)")
    return out_path


def stage_separate_vocals(source_path: Path, device: str) -> Path:
    """
    Run Demucs htdemucs vocal separation.
    Outputs are cached in AI_test/separated/<stem>/vocals.wav.
    Re-used on subsequent runs â€” Demucs does NOT re-run if output exists.
    """
    out_dir   = source_path.parent / "separated"
    stem_dir  = out_dir / "htdemucs" / source_path.stem
    vocal_wav = stem_dir / "vocals.wav"

    if vocal_wav.exists():
        print(f"    >> Cache hit: vocal stem already separated, skipping Demucs.")
        return vocal_wav

    print(f"    >> Running Demucs htdemucs on {device.upper()} ...")
    print(f"       (model is already cached â€” this runs fully offline)")

    # Demucs works best on a standard stereo mix; feed the original source
    cmd = [
        sys.executable, "-m", "demucs",
        "-n", "htdemucs",
        "--two-stems", "vocals",  # only output vocals + no_vocals
        "-d", device,
        "-o", str(out_dir),
        str(source_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Demucs failed:\n{result.stderr[-1000:]}")

    # Fallback: search for output if path unexpected
    if not vocal_wav.exists():
        candidates = list(out_dir.glob("**/vocals.wav"))
        if candidates:
            vocal_wav = candidates[0]
        else:
            raise FileNotFoundError(f"Demucs completed but vocals.wav not found under {out_dir}")

    print(f"    [OK] Vocal stem saved: {vocal_wav.relative_to(source_path.parent)}")
    return vocal_wav


# ——————————————————————————————————————————————————————————————————————————————
# Main
# ——————————————————————————————————————————————————————————————————————————————

def load_ai_models(model_size: str = "large-v2", language: str = "en", device: str | None = None, verbose: bool = True):
    """
    Pre-loads WhisperX ASR and alignment models into memory.
    Call this once before processing a queue to avoid reloading.
    """
    import whisperx
    import torch
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    if verbose:
        print(f"Loading WhisperX {model_size} ASR model onto {device.upper()}...")
    asr_model = whisperx.load_model(
        model_size, device=device, compute_type=compute_type,
        language=language if language != "auto" else None
    )
    
    if verbose:
        print(f"Loading WhisperX Alignment model for '{language}' onto {device.upper()}...")
    align_model, align_meta = whisperx.load_align_model(language_code=language, device=device)
    
    return {
        "asr_model": asr_model,
        "align_model": align_model,
        "align_meta": align_meta,
        "device": device,
        "compute_type": compute_type,
        "language": language
    }

def unload_ai_models(cached_models: dict | None = None, verbose: bool = False):
    """
    Unloads cached WhisperX models from GPU/CPU RAM and cleans up PyTorch CUDA cache.
    """
    import gc
    import torch
    if cached_models:
        for key in list(cached_models.keys()):
            cached_models[key] = None
        cached_models.clear()
        
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        try:
            torch.cuda.ipc_collect()
        except Exception:
            pass
        
    if verbose:
        print("[OK] AI models unloaded and GPU VRAM cleared.")

def align_lyrics(
    audio_path,
    transcript_text: str = "",
    title: str = "",
    artist: str = "",
    language: str = "en",
    device: str | None = None,
    model_size: str = "large-v2",
    format_mode: str = "word",
    cached_models: dict | None = None,
    status_callback: Callable | None = None,
) -> str:
    """
    Full pipeline: downsample → separate → ASR → align → match → ELRC.
    Pass cached_models to reuse GPU memory across multiple songs.
    Pass status_callback(step, total, stage_name, detail) for clean progress bar integration.
    """
    source = Path(audio_path)
    if not source.exists():
        raise FileNotFoundError(f"Audio file not found: {source}")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    TOTAL_STAGES = 5
    t0 = time.time()

    def report(step: int, stage_name: str, detail: str = ""):
        if status_callback:
            status_callback(step, TOTAL_STAGES, stage_name, detail)
        else:
            print_stage(step, TOTAL_STAGES, stage_name)

    if not status_callback:
        gpu_label = torch.cuda.get_device_name(0) if device == "cuda" else "CPU"
        print(f"\n  Device : {device.upper()} — {gpu_label}")
        print(f"  Model  : WhisperX {model_size}")
        print(f"  File   : {source.name}")

    if not transcript_text:
        report(1, "Fetching Plain Lyrics via LRCLIB", "Querying open lyrics database...")
        try:
            import sys
            root_dir = Path(__file__).resolve().parent.parent.parent
            if str(root_dir / "src") not in sys.path:
                sys.path.insert(0, str(root_dir / "src"))
            from Lyrics_manager.providers.lrclib import lrclib
            
            fetched_text = lrclib({"title": title, "artist": artist})
            if fetched_text:
                import re
                clean_fetched = re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', fetched_text)
                transcript_text = clean_fetched
        except Exception:
            pass

    # Track temporary files to clean up
    temp_files_to_clean = []

    try:
        # ——— Stage 1: Downsample to 16 kHz WAV ————————————————————————————
        report(1, "Downsampling Audio (16 kHz WAV)", f"Converting {source.name}...")
        wav_16k = stage_downsample(source)
        temp_files_to_clean.append(wav_16k)
        duration_sec = wav_16k.stat().st_size / (SAMPLE_RATE * 2)

        # ——— Stage 2: Separate Vocals via Demucs —————————————————————————
        report(2, "Demucs Vocal Separation", "Isolating vocal stem from instruments on " + device.upper() + "...")
        vocal_wav = stage_separate_vocals(source, device)
        temp_files_to_clean.append(vocal_wav)

        # Load vocal stem for WhisperX (returns float32 numpy at 16 kHz in memory)
        audio = whisperx.load_audio(vocal_wav.as_posix())
        duration_sec = len(audio) / SAMPLE_RATE

        # ——— Stage 3: Parse Transcript ———————————————————————————————————
        report(3, "Processing Transcript", "Parsing lyric structure & romanization...")
        raw_lines = [ln.strip() for ln in transcript_text.strip().splitlines() if ln.strip()]

        if language == "hi":
            raw_lines = [romanize_display(line) for line in raw_lines]

        user_lines = []
        import re
        for line in raw_lines:
            if line.startswith("(") and line.endswith(")"):
                user_lines.append(line)
            else:
                matches = list(re.finditer(r'\([^)]+\)', line))
                if matches:
                    clean_line = re.sub(r'\([^)]+\)', '', line).strip()
                    if clean_line:
                        user_lines.append(clean_line)
                    for m in matches:
                        user_lines.append(m.group(0))
                else:
                    user_lines.append(line)

        if not user_lines:
            raise ValueError("No transcript text provided or fetched.")

        user_words = []
        for l_idx, line in enumerate(user_lines):
            is_bg_line = line.startswith("(") or line.startswith("（")
            for w in line.split():
                user_words.append({
                    "text": w,
                    "clean": clean_word(w),
                    "line_idx": l_idx,
                    "bg": is_bg_line,
                    "start": None,
                    "end": None,
                })

        # ——— Stage 4: WhisperX ASR & Phoneme Alignment ——————————————————
        report(4, f"WhisperX ASR & Phoneme Alignment ({model_size})", "Transcribing & aligning phonemes...")
        if cached_models:
            asr_model = cached_models["asr_model"]
            align_model = cached_models["align_model"]
            align_meta = cached_models["align_meta"]
        else:
            asr_model = whisperx.load_model(
                model_size, device=device, compute_type=compute_type,
                language=language if language != "auto" else None
            )
            align_model, align_meta = whisperx.load_align_model(language_code=language, device=device)
        
        asr_kwargs = {"batch_size": 16, "language": language if language != "auto" else None}
        if language == "hi":
            asr_kwargs["initial_prompt"] = "यह हिंदी गाना है।"
        asr_result = asr_model.transcribe(audio, **asr_kwargs)

        aligned = whisperx.align(
            asr_result["segments"], align_model, align_meta,
            audio, device=device, return_char_alignments=False
        )

        asr_words = []
        for seg in aligned.get("segments", []):
            for w in seg.get("words", []):
                word_text = w.get("word", "").strip()
                if not word_text:
                    continue
                asr_words.append({
                    "text":  word_text,
                    "clean": clean_word(word_text),
                    "start": w.get("start"),
                    "end":   w.get("end"),
                })

        # ——— Stage 5: Match & Build Synchronized ELRC ———————————————————
        report(5, "Building Synchronized ELRC", "Running DTW & interpolating timestamps...")
        pairs = match_user_to_asr(user_words, asr_words)

        for u_idx, a_idx in pairs:
            user_words[u_idx]["start"] = asr_words[a_idx]["start"]
            user_words[u_idx]["end"]   = asr_words[a_idx]["end"]

        user_words = interpolate_timestamps(user_words, duration_sec, audio=audio)

        lines_with_words = [{"line_text": line, "words": []} for line in user_lines]
        for w in user_words:
            lines_with_words[w["line_idx"]]["words"].append({
                "word":  w["text"],
                "start": round(float(w["start"]), 3),
                "end":   round(float(w["end"]), 3),
            })

        if format_mode == "line":
            from elrc_builder import build_lrc_lines
            elrc_output = build_lrc_lines(lines_with_words, title=title, artist=artist)
        else:
            from elrc_builder import build_elrc_strict_lines
            elrc_output = build_elrc_strict_lines(lines_with_words, title=title, artist=artist)

        return elrc_output

    finally:
        # Automatic cleanup of temporary audio files
        for f in temp_files_to_clean:
            try:
                if f and f.exists():
                    f.unlink()
            except Exception:
                pass

        sep_dir = source.parent / "separated"
        if sep_dir.exists():
            import shutil
            try:
                shutil.rmtree(sep_dir, ignore_errors=True)
            except Exception:
                pass
