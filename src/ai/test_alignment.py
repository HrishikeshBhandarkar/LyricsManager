"""
STANDALONE WHISPERX AI FORCED ALIGNMENT TEST RUNNER:
Executes WhisperX forced alignment on a sample audio track and exports generated ELRC lyrics.
Features rich visual UI feedback showing every stage of the AI pipeline.
"""
import sys
import os
import time
from pathlib import Path

# Force HuggingFace to show download progress bars!
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"
os.environ["TQDM_DISABLE"] = "0"

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ai_test_dir = Path(__file__).resolve().parent
if str(ai_test_dir) not in sys.path:
    sys.path.insert(0, str(ai_test_dir))


def print_banner():
    import torch
    gpu_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if gpu_available else "Not Active (Running on CPU)"

    print()
    print("  +=========================================================+")
    print("  |                                                         |")
    print("  |   LYRICS MANAGER - AI FORCED ALIGNMENT ENGINE           |")
    print("  |         Powered by WhisperX | Word-by-Word ELRC         |")
    print("  |                                                         |")
    print("  +=========================================================+")
    print(f"  |  GPU Acceleration: {gpu_name:<36} |")
    print("  +=========================================================+")
    print()


def print_section(title: str):
    width = 55
    print(f"\n  {'-' * width}")
    print(f"  | {title}")
    print(f"  {'-' * width}")


def main():
    print_banner()

    # -- Detect Audio File -------------------------------------------------
    print_section("AUDIO FILE DETECTION")
    
    audio_extensions = {".mp3", ".flac", ".m4a", ".wav", ".ogg", ".opus", ".aac",".webm"}
    audio_files = [f for f in ai_test_dir.iterdir() if f.suffix.lower() in audio_extensions]
    
    if not audio_files:
        print("  [ERROR] No audio files found in AI_test/ directory!")
        print("  [TIP]   Place an audio file (MP3, FLAC, WAV, M4A) in:")
        print(f"          {ai_test_dir}")
        return

    if len(audio_files) == 1:
        sample_audio = audio_files[0]
    else:
        print(f"  Found {len(audio_files)} audio file(s):")
        for i, f in enumerate(audio_files, 1):
            size_kb = f.stat().st_size / 1024
            print(f"    [{i}] {f.name} ({size_kb:.1f} KB)")
        
        try:
            choice = input("\n  Select file number [1]: ").strip()
            idx = int(choice) - 1 if choice else 0
            sample_audio = audio_files[idx]
        except (ValueError, IndexError):
            sample_audio = audio_files[0]

    print(f"  [OK] Selected: {sample_audio.name}")
    print(f"  [OK] Path: {sample_audio}")

    # -- Transcript Input --------------------------------------------------
    print_section("TRANSCRIPT INPUT")
    
    txt_files = [f for f in ai_test_dir.iterdir() if f.suffix.lower() == ".txt"]
    
    transcript_text = ""
    
    if txt_files:
        print(f"  Found transcript file(s):")
        for i, f in enumerate(txt_files, 1):
            print(f"    [{i}] {f.name}")
        print(f"    [0] No transcript (let WhisperX transcribe automatically)")
        
        try:
            choice = input("\n  Select transcript [0 = auto-transcribe]: ").strip()
            if choice and int(choice) > 0:
                transcript_text = txt_files[int(choice) - 1].read_text(encoding="utf-8")
                print(f"  [OK] Loaded transcript ({len(transcript_text.split())} words)")
        except (ValueError, IndexError):
            pass

    if not transcript_text:
        print("  [INFO] No transcript provided -> WhisperX will auto-transcribe the audio!")
        print("  [INFO] The AI model will listen to the audio and generate lyrics automatically.")

    # -- Title & Artist ----------------------------------------------------
    print_section("METADATA")
    
    stem = sample_audio.stem
    if " - " in stem:
        parts = stem.split(" - ", 1)
        default_artist = parts[0].strip()
        default_title = parts[1].strip()
    else:
        default_title = stem
        default_artist = "Unknown Artist"
    
    try:
        title = input(f"  Title [{default_title}]: ").strip() or default_title
        artist = input(f"  Artist [{default_artist}]: ").strip() or default_artist
    except (EOFError, KeyboardInterrupt):
        title = default_title
        artist = default_artist
    
    print(f"  [OK] Title:  {title}")
    print(f"  [OK] Artist: {artist}")

    # -- Output Format -----------------------------------------------------
    print_section("OUTPUT FORMAT")
    print("  [1] Line-by-Line (Standard LRC)")
    print("  [2] Word-by-Word (Enhanced ELRC)")
    
    format_choice = input("\n  Select format [2]: ").strip()
    format_mode = "line" if format_choice == "1" else "word"
    print(f"  [OK] Selected format: {format_mode.upper()}\n")

    # -- Model Choice ------------------------------------------------------
    print_section("AI MODEL SELECTION")
    print("  [1] WhisperX Base (Fast, gets the job done)")
    print("  [2] WhisperX Large (More accuracy, takes longer)")
    
    model_choice = input("\n  Select model [2]: ").strip()
    model_size = "base" if model_choice == "1" else "large-v2"
    print(f"  [OK] Selected model: {model_size.upper()}\n")

    # -- Run Alignment -----------------------------------------------------
    print_section("STARTING WHISPERX AI ALIGNMENT PIPELINE")
    print(f"  >> Please wait -- the AI model is processing your audio...")
    print(f"  >> First run downloads model weights. Subsequent runs are cached.")
    
    t_start = time.time()
    
    from aligner import align_lyrics

    try:
        elrc_output = align_lyrics(
            audio_path=sample_audio,
            transcript_text=transcript_text,
            title=title,
            artist=artist,
            language="en",
            device=None,
            model_size=model_size,
            format_mode=format_mode
        )
    except Exception as e:
        print(f"\n  [FAILED] ALIGNMENT FAILED: {e}")
        print(f"  [TIP] Common fixes:")
        print(f"     - Make sure WhisperX is installed: pip install git+https://github.com/m-bain/whisperX.git")
        print(f"     - Make sure ffmpeg is installed and on PATH")
        print(f"     - Try a different audio file format (WAV or MP3)")
        import traceback
        traceback.print_exc()
        return

    elapsed = time.time() - t_start

    # -- Save Output -------------------------------------------------------
    print_section("SAVING OUTPUT")
    
    out_file = ai_test_dir / f"{sample_audio.stem}_aligned.elrc"
    out_file.write_text(elrc_output, encoding="utf-8")
    
    print(f"  [OK] Saved: {out_file.name}")
    print(f"  [OK] Path:  {out_file}")
    print(f"  [OK] Size:  {out_file.stat().st_size / 1024:.1f} KB")

    # -- Results Summary ---------------------------------------------------
    elrc_lines = [l for l in elrc_output.split("\n") if l.strip()]
    header_count = sum(1 for l in elrc_lines if l.startswith("[ti:") or l.startswith("[ar:") or l.startswith("[offset:") or l.startswith("[by:"))
    content_count = len(elrc_lines) - header_count
    
    print()
    print("  +=========================================================+")
    print("  |              ALIGNMENT COMPLETE!                         |")
    print("  +=========================================================+")
    print(f"  |  Total ELRC lines:     {content_count:<33} |")
    print(f"  |  Processing time:      {elapsed:.1f}s{' ' * (31 - len(f'{elapsed:.1f}s'))} |")
    print(f"  |  Output file:          {out_file.name:<33} |")
    print("  +=========================================================+")

    # -- Preview -----------------------------------------------------------
    print_section("ELRC PREVIEW (First 15 Lines)")
    for line in elrc_output.split("\n")[:15]:
        print(f"  | {line}")
    remaining = len(elrc_output.split("\n")) - 15
    if remaining > 0:
        print(f"  | ... ({remaining} more lines)")
    print()


if __name__ == "__main__":
    main()
