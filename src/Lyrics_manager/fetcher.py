import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pathlib import Path
import re

from .embedder import embed_lyrics
from .exporter import save_lyric_file

from .providers import (
    lrclib,
    biniLy,
    musixmatch_provider,
    syncedlyrics_provider,
    paxsenix,
    kugou_provider,
    parse_krc_to_elrc,
    netease_provider,
    qqmusic_provider,
    is_truly_enhanced,
    ms_to_lrc_time_3,
)


"""
MY FETCHER MODULE ARCHITECTURE & PIPELINE OVERVIEW:
- Purpose: This module is my central engine for routing, formatting, and exporting music lyrics.
- Provider logic has been split into individual modules under the providers/ package.
- This file contains:
    1. format_to_reference_elrc() - Universal reference ELRC formatter
    2. api_calls() - Main router pipeline
    3. main() - Interactive CLI tester & exporter
"""


# =====================================================================
# MY UNIVERSAL REFERENCE ELRC FORMATTER ENGINE
# =====================================================================

def format_to_reference_elrc(lyrics_str: str, title: str = "", artist: str = "") -> str:
    """
    MY UNIVERSAL REFERENCE ELRC FORMATTER:
    Normalizes any provider's ELRC/LRC output to strictly match the reference formatting specification in Just Keep Watching - Tate McRae.lrc.
    - Header Tags: [ti:...], [ar:...], [offset:+0], [by:Generated using LyricsManager (https://github.com/HrishikeshBhandarkar/LyricsManager)]
    - 3-Decimal Timestamps: [MM:SS.mmm] and <MM:SS.mmm>
    - Word-by-Word Lines: [MM:SS.mmm]v1:<MM:SS.mmm>Word <MM:SS.mmm>by ... <MM:SS.mmm>
    - Line-Synced Lines (no word timestamps): [MM:SS.mmm] Lyrics text here (NO v1 tag!)
    - Background Vocal Lines: [bg:<MM:SS.mmm>Yeah, <MM:SS.mmm>yeah ... <MM:SS.mmm>]
    """
    if not lyrics_str or not lyrics_str.strip():
        return ""

    lines = lyrics_str.strip().split("\n")
    header_lines = []
    content_lines = []

    if title:
        header_lines.append(f"[ti:{title}]")
    if artist:
        header_lines.append(f"[ar:{artist}]")
    header_lines.append("[offset:+0]")
    header_lines.append("[by:Generated using LyricsManager (https://github.com/HrishikeshBhandarkar/LyricsManager)]")

    # Helper function to convert float or string timestamp mm:ss.xx/xxx to 3-decimal MM:SS.mmm
    def norm_ts_match(m):
        mins = int(m.group(1))
        secs = int(m.group(2))
        raw_ms = m.group(3) or "0"
        ms_val = float("0." + raw_ms)
        total_ms = int(mins * 60000 + secs * 1000 + ms_val * 1000)
        return ms_to_lrc_time_3(total_ms)

    for line_str in lines:
        line = line_str.strip()
        if not line:
            continue

        # Skip existing metadata header tags if present in input string
        if line.startswith(("[ti:", "[ar:", "[al:", "[by:", "[offset:", "[re:", "[ve:")):
            continue

        # 1. Normalize all [MM:SS.xx] and <MM:SS.xx> timestamps to 3 decimal places
        line = re.sub(
            r"\[(\d{2}):(\d{2})(?:\.(\d+))?\]",
            lambda m: f"[{norm_ts_match(m)}]",
            line
        )
        line = re.sub(
            r"\<(\d{2}):(\d{2})(?:\.(\d+))?\>",
            lambda m: f"<{norm_ts_match(m)}>",
            line
        )

        # 2. Check vocal tags
        is_bg = line.startswith("[bg:") or line.startswith("[bg]")
        is_v2 = False

        line = re.sub(r"^\[bg:?\s*", "", line, flags=re.IGNORECASE)
        line = re.sub(r"^\[bg\]\s*", "", line, flags=re.IGNORECASE)
        if is_bg:
            line = re.sub(r"\]$", "", line)

        # Extract leading line timestamp tag [MM:SS.mmm] if present
        line_ts_match = re.match(r"^\[(\d{2}:\d{2}\.\d{3})\]", line)
        line_ts_tag = ""
        if line_ts_match:
            line_ts_tag = line_ts_match.group(0)
            line = line[len(line_ts_tag):].strip()

        if re.match(r"^v[12]", line, flags=re.IGNORECASE):
            if line.lower().startswith("v2"):
                is_v2 = True
            line = re.sub(r"^v[12][:<\s]*", "", line, flags=re.IGNORECASE)
            if "<" in line and not line.startswith("<"):
                line = "<" + line

        line = re.sub(r"^\[v[12]\]\s*", "", line, flags=re.IGNORECASE)
        line = line.strip()

        # 3. Determine if this line has word-level timestamps (<MM:SS.mmm>)
        has_word_timestamps = bool(re.search(r"<\d{2}:\d{2}\.\d{2,3}>", line))

        if is_bg:
            content_lines.append(f"[bg:{line}]")
        elif has_word_timestamps:
            # Word-by-word enhanced line -> add v1:/v2: prefix
            role_prefix = "v2:" if is_v2 else "v1:"
            if line_ts_tag:
                content_lines.append(f"{line_ts_tag}{role_prefix}{line}")
            else:
                content_lines.append(f"{role_prefix}{line}")
        else:
            # Line-synced only -> NO v1/v2 tag, just [timestamp] text
            if line_ts_tag:
                content_lines.append(f"{line_ts_tag} {line}")
            else:
                content_lines.append(line)

    return "\n".join(header_lines + content_lines)


# =====================================================================
# MY MAIN ROUTER PIPELINE FUNCTION
# =====================================================================
def api_calls(data: dict[int, dict], type: str, how: str) -> tuple[dict, dict]:
    """
    MY MAIN API ROUTER FUNCTION:
    Takes parsed tracks dictionary from data4api.py module and routes requests according to precision rules.
    - Enhanced Mode ('enhanced' / 'word'):
        1. BiniLyrics Word TTML (Priority #1)
        2. KuGou KRC Word-by-Word ELRC (Priority #2)
        3. NetEase YRC Word-by-Word ELRC (Priority #3)
        4. QQ Music QRC Word-by-Word ELRC (Priority #4)
        5. Musixmatch RichSync (Priority #5 - Swapped above Paxsenix)
        6. Paxsenix Apple Music ELRC (Priority #6 - Swapped below Musixmatch)
        7. Memory / LRCLIB Line Fallback
    - Standard Mode ('standard' / 'line'):
        1. LRCLIB Line (Priority #1)
        2. SyncedLyrics Library (Megalobiz / Deezer) (Priority #2)
        3. KuGou Line (Priority #3)
        4. NetEase Line (Priority #4 - Above QQ Music)
        5. QQ Music Line (Priority #5 - Below NetEase)
        6. Musixmatch Line (Priority #6)
    Returns tuple of dictionaries: (found_lyrics_dict, failed_lyrics_dict)
    """
    found_lyrics = {}
    failed_lyrics = {}

    type_norm = type.lower().strip()

    for track_id, track in data.items():
        lyrics = ""
        source_used = ""

        # MY ROUTING PIPELINE BASED ON DESIRED LYRIC PRECISION:
        if type_norm in ("enhanced", "word"):
            fallback_line_lyric = ""
            fallback_source = ""

            # Step 1: Query BiniLyrics Word (Priority #1)
            lyrics = biniLy(track, "enhanced")
            if lyrics and is_truly_enhanced(lyrics):
                source_used = "BiniLyrics (Word)"
            elif lyrics and ("[" in lyrics and "]" in lyrics):
                if not fallback_line_lyric:
                    fallback_line_lyric = lyrics
                    fallback_source = "BiniLyrics (Line Fallback)"
                lyrics = ""

            # Step 2: Query KuGou KRC Word (Priority #2)
            if not lyrics:
                lyrics = kugou_provider(track, "enhanced")
                if lyrics and is_truly_enhanced(lyrics):
                    source_used = "KuGou (KRC Word)"
                elif lyrics and ("[" in lyrics and "]" in lyrics):
                    if not fallback_line_lyric:
                        fallback_line_lyric = lyrics
                        fallback_source = "KuGou (Line Fallback)"
                    lyrics = ""

            # Step 3: Query NetEase YRC Word (Priority #3 - Above QQ Music)
            if not lyrics:
                lyrics = netease_provider(track, "enhanced")
                if lyrics and is_truly_enhanced(lyrics):
                    source_used = "NetEase (YRC Word)"
                elif lyrics and ("[" in lyrics and "]" in lyrics):
                    if not fallback_line_lyric:
                        fallback_line_lyric = lyrics
                        fallback_source = "NetEase (Line Fallback)"
                    lyrics = ""

            # Step 4: Query QQ Music QRC Word (Priority #4 - Below NetEase)
            if not lyrics:
                lyrics = qqmusic_provider(track, "enhanced")
                if lyrics and is_truly_enhanced(lyrics):
                    source_used = "QQ Music (QRC Word)"
                elif lyrics and ("[" in lyrics and "]" in lyrics):
                    if not fallback_line_lyric:
                        fallback_line_lyric = lyrics
                        fallback_source = "QQ Music (Line Fallback)"
                    lyrics = ""

            # Step 5: Query Musixmatch RichSync (Priority #5 - Swapped above Paxsenix)
            if not lyrics:
                lyrics = musixmatch_provider(track, "enhanced")
                if lyrics and is_truly_enhanced(lyrics):
                    source_used = "Musixmatch (RichSync)"
                elif lyrics and ("[" in lyrics and "]" in lyrics):
                    if not fallback_line_lyric:
                        fallback_line_lyric = lyrics
                        fallback_source = "Musixmatch (Line Fallback)"
                    lyrics = ""

            # Step 6: Query Paxsenix Apple Music ELRC (Priority #6 - Swapped below Musixmatch)
            if not lyrics:
                lyrics = paxsenix(track)
                if lyrics and is_truly_enhanced(lyrics):
                    source_used = "Paxsenix (Apple Music ELRC)"
                elif lyrics and ("[" in lyrics and "]" in lyrics):
                    if not fallback_line_lyric:
                        fallback_line_lyric = lyrics
                        fallback_source = "Paxsenix (Line Fallback)"
                    lyrics = ""

            # Fallback check: If no word lyrics were found across top 6 providers, use stored line lyric from memory
            if not lyrics:
                if fallback_line_lyric:
                    lyrics = fallback_line_lyric
                    source_used = fallback_source
                else:
                    # Fallback to LRCLIB if no line lyric was captured in memory
                    lyrics = lrclib(track)
                    if lyrics:
                        source_used = "LRCLIB (Fallback)"

        else:
            # Standard Line-Synced Mode requested by user
            # Step 1: Query LRCLIB (Primary contender for standard lyrics)
            lyrics = lrclib(track)
            if lyrics:
                source_used = "LRCLIB"
            else:
                # Step 2: Query SyncedLyrics library (NetEase / Megalobiz / Deezer)
                lyrics = syncedlyrics_provider(track)
                if lyrics:
                    source_used = "SyncedLyrics Library"
                else:
                    # Step 3: Query KuGou Line-synced (Priority #3)
                    lyrics = kugou_provider(track, "standard")
                    if lyrics:
                        source_used = "KuGou (Line)"
                    else:
                        # Step 4: Query NetEase Line-synced (Priority #4 - Above QQ Music)
                        lyrics = netease_provider(track, "standard")
                        if lyrics:
                            source_used = "NetEase (Line)"
                        else:
                            # Step 5: Query QQ Music Line-synced (Priority #5 - Below NetEase)
                            lyrics = qqmusic_provider(track, "standard")
                            if lyrics:
                                source_used = "QQ Music (Line)"
                            else:
                                # Step 6: Fallback to Musixmatch Line
                                lyrics = musixmatch_provider(track, "standard")
                                if lyrics:
                                    source_used = "Musixmatch (Line)"

        # Record output in respective result dictionaries & execute delivery method
        if lyrics:
            formatted_lyrics = format_to_reference_elrc(lyrics, title=track.get("title", ""), artist=track.get("artist", ""))
            
            output_status = False
            how_norm = how.lower().strip()
            if how_norm == "sep":
                saved_path = save_lyric_file(track["path"], formatted_lyrics)
                output_status = bool(saved_path)
            elif how_norm == "emb":
                output_status = embed_lyrics(track["path"], formatted_lyrics)

            found_lyrics[track_id] = {
                "title": track["title"],
                "artist": track["artist"],
                "lyrics": formatted_lyrics,
                "path": track["path"],
                "how": how,
                "type": type_norm,
                "source": source_used,
                "saved_ok": output_status
            }
        else:
            failed_lyrics[track_id] = {
                "title": track["title"],
                "artist": track["artist"],
                "path": track["path"],
                "reason": "No lyrics found across available providers"
            }

    return found_lyrics, failed_lyrics


# =====================================================================
# MY MULTI-API CLI TESTER & EXPORTER
# =====================================================================

def main():
    """
    MY STANDARDIZED MULTI-API CLI TESTER & AI GENERATOR:
    Provides a main menu to either fetch lyrics from APIs or generate them via AI Forced Alignment.
    """
    print("=================================================================")
    print("    MY LYRIC MANAGER - MULTI-API PROVIDER & AI ALIGNMENT        ")
    print("=================================================================")
    print("  [1] Search Web APIs for Lyrics (NetEase, KuGou, Musixmatch...)")
    print("  [2] Generate AI Synchronized Lyrics (WhisperX)")
    
    try:
        mode = input("\nSelect mode [1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        return

    if mode == "1":
        _run_api_fetcher()
    elif mode == "2":
        _run_ai_aligner()
    else:
        print("Invalid choice.")


api_providers = [
    ("BiniLyrics (Apple Music)", "output_binilyrics.elrc", lambda t: biniLy(t, "enhanced")),
    ("KuGou", "output_kugou.elrc", lambda t: kugou_provider(t, "enhanced")),
    ("NetEase", "output_netease.elrc", lambda t: netease_provider(t, "enhanced")),
    ("QQ Music", "output_qqmusic.elrc", lambda t: qqmusic_provider(t, "enhanced")),
    ("Musixmatch", "output_musixmatch.elrc", lambda t: musixmatch_provider(t, "enhanced")),
    ("Paxsenix", "output_paxsenix.elrc", lambda t: paxsenix(t)),
    ("LRCLIB", "output_lrclib.lrc", lambda t: lrclib(t)),
]

def _run_api_fetcher():
    default_title = "São Paulo"
    default_artist = "The Weeknd"

    try:
        user_title = input(f"\nEnter song title [{default_title}]: ").strip()
        user_artist = input(f"Enter artist name [{default_artist}]: ").strip()
        desired_format = input("Desired format? [1] Line-by-Line [2] Word-by-Word (default 2): ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    title = user_title if user_title else default_title
    artist = user_artist if user_artist else default_artist
    format_req = "line" if desired_format == "1" else "word"
    
    # We simulate a "queue" of 1 song for now to demonstrate the architecture
    song_queue = [{"title": title, "artist": artist, "path": f"{title}.wav", "duration_ms": 210000}]
    suboptimal_queue = []

    print(f"\nProcessing queue of {len(song_queue)} song(s)...\n")

    test_dir = Path(__file__).resolve().parent.parent.parent / "Test"
    test_dir.mkdir(parents=True, exist_ok=True)

    for track in song_queue:
        print(f"\nSearching APIs for: '{track['title']}' by '{track['artist']}'...")
        print(f"{'PROVIDER':<15} | {'STATUS':<20} | {'SAVED OUTPUT FILE'}")
        print("-" * 65)

        best_found_format = None
        
        for name, filename, fn in api_providers:
            try:
                raw_res = fn(track)
                if raw_res:
                    formatted_res = format_to_reference_elrc(raw_res, title=track["title"], artist=track["artist"])
                    is_enh = is_truly_enhanced(formatted_res)
                    status_str = "WORD-BY-WORD (ELRC)" if is_enh else "LINE-SYNCED (LRC)"
                    out_path = test_dir / filename
                    out_path.write_text(formatted_res, encoding="utf-8")
                    print(f"{name:<15} | {status_str:<20} | {out_path.name}")
                    
                    if is_enh and best_found_format != "word":
                        best_found_format = "word"
                    elif not is_enh and not best_found_format:
                        best_found_format = "line"
                else:
                    print(f"{name:<15} | {'NOT FOUND':<20} | -")
            except Exception as e:
                print(f"{name:<15} | {f'ERROR ({e})':<20} | -")

        print("-" * 65)
        
        if format_req == "word" and best_found_format != "word":
            print(f"[!] '{track['title']}' did NOT fulfill '{format_req}' requirement (Got: {best_found_format or 'None'})")
            suboptimal_queue.append(track)
        elif not best_found_format:
            print(f"[!] '{track['title']}' yielded no lyrics.")
            suboptimal_queue.append(track)

    if suboptimal_queue:
        print(f"\n[!] {len(suboptimal_queue)} song(s) did not meet your requested format.")
        for s in suboptimal_queue:
            print(f"  - {s['title']} by {s['artist']}")
        
        ans = input("\nDo you want to run these through the AI Generator? (y/n) [y]: ").strip().lower()
        if ans != 'n':
            _run_ai_fallback_queue(suboptimal_queue, format_req)


AI_ENGAGEMENT_TIPS = [
    # --- Whisper & WhisperX Architecture ---
    "◆ [Whisper Architecture] OpenAI's Whisper converts audio waveforms into 80-channel log-Mel spectrograms before feeding them into an encoder-decoder Transformer.",
    "◆ [Why WhisperX?] Standard Whisper outputs rough chunk timestamps (~30s). WhisperX uses Wav2Vec2 phonetic alignment to pinpoint individual words to milliseconds!",
    "◆ [Phoneme Alignment] Wav2Vec2 predicts probability distributions over phonetic tokens (phonemes) across time frames using CTC loss.",
    "◆ [Dynamic Time Warping] Lyric Manager matches the official lyrics to WhisperX's phonetic output using global Needleman-Wunsch Dynamic Time Warping (DTW)!",
    "◆ [Voice Activity Detection] Pyannote VAD detects speech vs silence so Whisper doesn't hallucinate during long instrumental intros.",
    "◆ [Multi-Head Attention] Multi-head self-attention allows the neural net to focus on different frequency harmonics of the singer's voice simultaneously.",
    "◆ [Int8 vs FP16] FP16 gives maximum GPU precision, while Int8 quantization cuts VRAM usage in half with negligible accuracy loss.",
    "◆ [Whisper Large-V2] Trained on 680,000 hours of multilingual audio, containing over 1.5 billion parameters!",
    "◆ [Acapella Isolation] By aligning exclusively on clean acapella stems, WhisperX avoids confusing vocal harmonies with brass or guitar solos.",
    "◆ [Monotone Interpolation] If a backing vocal or ad-lib is inaudible, Lyric Manager uses monotone linear interpolation to maintain seamless karaoke pacing.",
    "◆ [Multilingual Sync] WhisperX supports over 90 languages including English, Hindi, Spanish, Japanese, Korean, French, and German!",
    "◆ [Devanagari & Romanization] Hindi and Bollywood songs are dynamically normalized into Latin Hinglish phonemes for flawless cross-language alignment.",
    "◆ [Acoustic Energy Tracking] When a singer holds a vowel at the end of a line, RMS energy tracking prevents the timestamp from cutting off prematurely.",

    # --- Demucs & Audio Source Separation ---
    "◆ [How Demucs Works] Demucs HT (Hybrid Transformer) combines time-domain U-Nets with frequency-domain Transformers to separate vocals from instruments.",
    "◆ [Phase Cancellation] Modern source separation neural nets predict complex spectrogram masks that isolate vocals via inverse Short-Time Fourier Transforms (iSTFT).",
    "◆ [Instrumental Stripping] Drums and heavy bass share the same fundamental frequencies as human speech, which can throw off standard speech recognizers.",
    "◆ [16 kHz Downsampling] Speech recognition models are standardly trained on 16 kHz audio because the human vocal range sits comfortably below the 8 kHz Nyquist limit.",
    "◆ [Audio Normalization] Acapella tracks are dynamically normalized to 0 dB peak to boost soft whispered lyrics for the aligner.",
    "◆ [Demucs 4-Stem Model] Demucs can split full stereo mixes into 4 discrete audio stems: Vocals, Drums, Bass, and Other (synths/guitars).",
    "◆ [Lossless Audio] Aligning on lossless FLAC/WAV files provides cleaner high-frequency vocal transients compared to low-bitrate MP3s.",

    # --- LLM Prompting & AI Mechanics ---
    "◆ [Few-Shot Prompting] Providing 2-3 input/output examples inside an LLM prompt dramatically increases accuracy on complex formatting tasks compared to Zero-Shot.",
    "◆ [Chain-of-Thought] Asking an LLM to 'think step-by-step' forces it to generate intermediate reasoning tokens, preventing logical leaps and calculation errors.",
    "◆ [Temperature in LLMs] Setting temperature close to 0 makes LLM outputs deterministic and factual, while temperature > 0.7 introduces creative variance.",
    "◆ [System Prompts] The system prompt sets the foundational personality, guardrails, and role constraints for an AI before user conversation begins.",
    "◆ [Tokenization] LLMs don't read words or letters directly — they process 'tokens' (sub-word chunks). On average, 1,000 tokens equals roughly 750 English words.",
    "◆ [KV Caching] During LLM generation, previous Key-Value attention tensors are cached in GPU memory so the model doesn't recompute the entire prompt on every new token!",
    "◆ [RLHF Alignment] Tunes raw foundational models using reward models trained on human preferences to be helpful, concise, and safe.",
    "◆ [Top-P Sampling] Limits selectable next tokens to the smallest set whose cumulative probability exceeds P (e.g. 0.9), filtering out low-probability nonsense.",
    "◆ [Context Windows] The maximum number of tokens an LLM can pay attention to at once. Modern models handle anywhere from 8k to over 2 million tokens!",
    "◆ [Role Prompting] Telling an AI 'You are a senior sound engineer' steers its latent vector representations towards specialized technical vocabulary.",
    "◆ [Prompt Injection] A vulnerability where untrusted user input hijacks the system prompt's instructions — robust apps isolate and sanitize prompt delimiters.",
    "◆ [Autoregressive Generation] LLMs predict text one token at a time, appending each newly generated token back to its own input for the next step.",
    "◆ [Embedding Vectors] Embeddings map text or audio into high-dimensional vector space where semantically similar concepts cluster close together mathematically.",
    "◆ [Residual Connections] Residual skip connections allow gradients to flow directly through deep neural networks without vanishing during backpropagation.",
    "◆ [Quantization] Compressing 16-bit neural weights into 4-bit or 8-bit integers enables giant models to run on consumer laptops and phones!",

    # --- Interactive Questions & Friendly Prompts ---
    "◆ [Question] How is the weather outside today where you are? Perfect day to curate your music library!",
    "◆ [Coffee Break] Taking a coffee or tea break? The AI is crunching millions of neural matrix multiplications right now.",
    "◆ [Music Genre] What genre of music are you syncing? Rock, hip-hop, electronic, pop, metal, or classical?",
    "◆ [Album Check] Have you listened to this whole album, or is this your favorite track from the artist?",
    "◆ [Music Player] What music player do you use? Apple Music, Spotify, Poweramp, Foobar2000, or Symfonium?",
    "◆ [Question] Do you prefer word-by-word karaoke bouncing ball lyrics or clean line-by-line synced lyrics?",
    "◆ [Relax] Sit back and relax — neural audio processing takes a moment to ensure pixel-perfect timing.",
    "◆ [Trivia] Synced lyrics created in ELRC format are compatible with Apple Music, Musixmatch, and modern mobile music players.",
    "◆ [Trivia] Which artist has the fastest lyrics in your music library? Eminem, Busta Rhymes, or someone else?",
    "◆ [Tip] You can run '/config' anytime to switch between Whisper Base (super fast) and Large-V2 (ultra accurate).",
    "◆ [Trivia] Listening to music in the morning or unwinding late at night? Syncing your library makes every listen better.",
    "◆ [Guitar Solos] Is there a guitar or drum solo in this song? Demucs filters it out so the vocal aligner stays laser focused.",
    "◆ [Offline Lyrics] Embedding lyrics directly into the audio file means they display offline on any device without internet!",

    # --- Audio & Lyrics Formats Trivia ---
    "◆ [LRC vs ELRC] Standard LRC only timestamps line beginnings [01:23.45]. ELRC (Enhanced LRC) embeds intra-line word timestamps <01:23.45>word.",
    "◆ [ID3 Tagging] ID3v2 tags store unsynchronized lyrics in USLT frames, while synchronized line/word timestamps live in SYLT frames.",
    "◆ [Vorbis Comments] FLAC and OGG files store lyrics in the 'LYRICS' or 'UNSYNCEDLYRICS' metadata blocks encoded in UTF-8.",
    "◆ [Millisecond Precision] Lyric Manager formats timestamps to 3 decimal places (e.g. 00:12.340) for buttery-smooth animations in modern lyric viewers.",
    "◆ [LRCLIB Database] LRCLIB is a community-driven open-source lyric archive providing synchronized and plain text lyrics to millions of apps.",
    "◆ [Headphone Check] Are you listening on audiophile IEMs, open-back headphones, or speakers right now?",
    "◆ [GPU Acceleration] On NVIDIA RTX GPUs, CUDA Tensor Cores accelerate WhisperX matrix multiplications by over 10x compared to CPU execution!"
]

def _run_ai_fallback_queue(queue, format_mode, save_choice: str = "3"):
    import sys
    import time
    import random
    import warnings
    warnings.filterwarnings("ignore")
    
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    
    console = Console()
    
    root_dir = Path(__file__).resolve().parent.parent.parent
    ai_dir = root_dir / "src" / "ai"
    if str(ai_dir) not in sys.path:
        sys.path.insert(0, str(ai_dir))
        
    try:
        from aligner import align_lyrics, load_ai_models, unload_ai_models
    except ImportError as e:
        console.print(f"\n[bold red][ERROR] Could not import AI aligner: {e}[/bold red]")
        return
        
    try:
        from Lyrics_manager.config import get_whisper_model_size
        model_size = get_whisper_model_size()
    except ImportError:
        model_size = "large-v2"

    try:
        from Lyrics_manager.embedder import embed_lyrics
    except ImportError:
        embed_lyrics = None

    console.print("\n[bold color(208)]--- AI FORCED ALIGNMENT ENGINE ---[/bold color(208)]")
    console.print("[grey70]✦ [bold yellow]Note:[/bold yellow] AI Forced Alignment works best with [bold white]English[/bold white]; other languages can be hit-or-miss depending on vocal clarity.[/grey70]\n")
    
    # Pre-load AI models with a sleek spinner
    with console.status(f"[bold white]Pre-loading AI Models ([bold color(208)]{model_size}[/bold color(208)]) to GPU/CPU...[/bold white]", spinner="dots"):
        cached_models = load_ai_models(model_size=model_size, verbose=False)
    console.print("[bold green]✔ AI Models pre-loaded and cached in memory![/bold green]\n")

    results_summary = []

    with Progress(
        SpinnerColumn(style="color(208)"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=45, complete_style="green", finished_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        
        master_task = progress.add_task(f"Batch AI Syncing ({len(queue)} songs)...", total=len(queue))
        
        # Dedicated live ticker task rendered on its own line
        import threading
        stop_ticker = threading.Event()
        current_tip = [random.choice(AI_ENGAGEMENT_TIPS)]
        used_tips = set(current_tip)
        tip_task = progress.add_task(f"[grey70]>> {current_tip[0]}[/grey70]", total=None)
        
        def ticker_loop():
            while not stop_ticker.is_set():
                if stop_ticker.wait(25.0):
                    break
                avail = [t for t in AI_ENGAGEMENT_TIPS if t not in used_tips]
                if not avail:
                    used_tips.clear()
                    avail = AI_ENGAGEMENT_TIPS
                new_tip = random.choice(avail)
                used_tips.add(new_tip)
                current_tip[0] = new_tip
                try:
                    progress.update(tip_task, description=f"[grey70]>> {new_tip}[/grey70]")
                except Exception:
                    pass
                    
        ticker_thread = threading.Thread(target=ticker_loop, daemon=True)
        ticker_thread.start()
        
        try:
            for idx, track in enumerate(queue):
                title = track.get("title", "Unknown")
                artist = track.get("artist", "Unknown")
                
                # Audio path resolution
                if "path" in track and track["path"] and Path(track["path"]).exists():
                    audio_path = str(track["path"])
                else:
                    progress.stop()
                    audio_path = Prompt.ask(f"[bold color(208)]Enter audio path for '{title}'[/bold color(208)]").strip()
                    progress.start()
                    
                if not audio_path or not Path(audio_path).exists():
                    results_summary.append((title, artist, "[red]Invalid Audio Path[/red]"))
                    progress.advance(master_task)
                    continue

                audio_file = Path(audio_path)
                out_dir = audio_file.parent
                
                progress.update(master_task, description=f"Processing [{idx+1}/{len(queue)}]: {title}...")
                
                # Create subtask for this song's 5 stages
                song_task = progress.add_task(f"Initializing '{title}'...", total=5)
                
                def status_cb(step_num, total_steps, stage_name, detail=""):
                    progress.update(
                        song_task, 
                        completed=step_num, 
                        description=f"[color(208)][{step_num}/{total_steps}][/color(208)] {stage_name}"
                    )
                    
                transcript_text = track.get("transcript", "")
                t_start = time.time()
                
                try:
                    elrc_output = align_lyrics(
                        audio_path=audio_path,
                        transcript_text=transcript_text,
                        title=title,
                        artist=artist,
                        language="en",
                        device=None,
                        model_size=model_size,
                        format_mode=format_mode,
                        cached_models=cached_models,
                        status_callback=status_cb
                    )
                    
                    elapsed = time.time() - t_start
                    ext = ".lrc" if format_mode == "line" else ".elrc"
                    
                    clean_name = "".join([c for c in f"{title} - {artist}" if c.isalpha() or c.isdigit() or c in " -_"]).rstrip()
                    if not clean_name:
                        clean_name = audio_file.stem
                        
                    out_path = out_dir / f"{clean_name}{ext}"
                    
                    # Sidecar file
                    if save_choice in ["2", "3"]:
                        out_path.write_text(elrc_output, encoding="utf-8")
                        
                    # Embedding
                    is_embedded = False
                    if save_choice in ["1", "3"] and embed_lyrics:
                        try:
                            embed_lyrics(str(audio_path), elrc_output)
                            is_embedded = True
                        except Exception:
                            pass
                            
                    embed_label = " + Embedded" if is_embedded else ""
                    results_summary.append((title, artist, f"[green]Synced ({elapsed:.1f}s){embed_label}[/green]"))
                    
                except Exception as e:
                    results_summary.append((title, artist, f"[red]Failed: {e}[/red]"))
                    
                progress.remove_task(song_task)
                progress.advance(master_task)
                
            progress.update(master_task, description="[bold green]Batch AI Synchronization Complete![/bold green]")
        finally:
            stop_ticker.set()
            ticker_thread.join(timeout=1.0)
            try:
                progress.remove_task(tip_task)
            except Exception:
                pass

    # Unload AI Models & Free GPU VRAM
    with console.status("[bold white]Unloading AI models & freeing GPU VRAM...[/bold white]", spinner="dots"):
        unload_ai_models(cached_models)
    console.print("[bold green]✔ AI models successfully unloaded & GPU/CPU RAM cleared![/bold green]")

    # Print Summary Table
    console.print("\n[bold color(208)]--- AI BATCH SUMMARY ---[/bold color(208)]")
    summary_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    summary_table.add_column("Song", style="bold white", width=28)
    summary_table.add_column("Artist", style="grey70", width=20)
    summary_table.add_column("Status", style="green")
    
    for s_title, s_artist, s_status in results_summary:
        summary_table.add_row(s_title, s_artist, s_status)
        
    console.print(Panel(summary_table, border_style="color(208)", title="[bold white]Generated Lyrics[/bold white]", title_align="left"))
    console.print()

if __name__ == "__main__":
    main()
