"""
EXPORT PROCESSED VOCAL AUDIO FOR INSPECTION
================────────────────────────────
This script runs the exact Demucs vocal separation and enhancement chain 
used by the aligner, and exports the final 16kHz mono WAV audio file 
so you can listen to what the AI model actually hears.
"""
import sys
import os
import time
import subprocess
from pathlib import Path
import scipy.io.wavfile as wavfile
import numpy as np

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"
os.environ["TQDM_DISABLE"] = "0"

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ai_test_dir = Path(__file__).resolve().parent
if str(ai_test_dir) not in sys.path:
    sys.path.insert(0, str(ai_test_dir))

import whisperx

import torch

def main():
    print("=" * 65)
    print("        EXPORTER: 16kHz MONO PROCESSED VOCAL AUDIO")
    print("=" * 65)

    if len(sys.argv) > 1:
        sample_audio = Path(sys.argv[1])
    else:
        audio_extensions = {".mp3", ".flac", ".m4a", ".wav", ".ogg", ".opus", ".aac"}
        audio_files = [f for f in ai_test_dir.iterdir() if f.suffix.lower() in audio_extensions and not f.name.endswith("_processed_vocal_16k.wav") and not f.name.endswith("_16k.wav")]

        if not audio_files:
            print("[ERROR] No input audio files found in AI_test/ directory!")
            return

        print("Found audio file(s):")
        for i, f in enumerate(audio_files, 1):
            print(f"  [{i}] {f.name}")

        if len(audio_files) == 1:
            sample_audio = audio_files[0]
        else:
            try:
                choice = input(f"\nSelect file number [1]: ").strip()
                idx = int(choice) - 1 if choice else 0
                sample_audio = audio_files[idx]
            except (ValueError, IndexError):
                sample_audio = audio_files[0]

    print(f"\n[OK] Processing file: {sample_audio.name}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    out_dir = sample_audio.parent / "separated"
    model = "htdemucs"
    vocal_stem = out_dir / model / sample_audio.stem / "vocals.wav"

    if not vocal_stem.exists():
        print(f">> Running Demucs htdemucs separation on {device.upper()}...")
        cmd = [
            sys.executable, "-m", "demucs",
            "-n", model,
            "--two-stems", "vocals",
            "-d", device,
            "-o", str(out_dir),
            str(sample_audio)
        ]
        subprocess.run(cmd, check=True)

    print(f">> Loading 16kHz mono audio from separated vocal stem...")
    raw_vocal = whisperx.load_audio(vocal_stem.as_posix())

    # Convert float32 [-1.0, 1.0] to int16 PCM WAV
    pcm_audio = (raw_vocal * 32767.0).astype(np.int16)

    output_wav = ai_test_dir / f"{sample_audio.stem}_processed_vocal_16k.wav"
    wavfile.write(str(output_wav), 16000, pcm_audio)

    print("\n" + "=" * 65)
    print(" [SUCCESS] EXPORT COMPLETE!")
    print(f" Saved file: {output_wav.name}")
    print(f" Full path:  {output_wav}")
    print(" You can now open and play this WAV file to hear the exact vocal audio fed to the AI.")
    print("=" * 65)

if __name__ == "__main__":
    main()
