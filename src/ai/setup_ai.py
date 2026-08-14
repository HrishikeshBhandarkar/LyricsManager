"""
ONE-CLICK SETUP: downloads & caches all WhisperX model weights.
Run this once before using the alignment tool.
"""
import os
import sys
import time
import shutil

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"
os.environ["TQDM_DISABLE"] = "0"


def banner():
    print("=" * 60)
    print("     LYRICS MANAGER — WhisperX AI ONE-CLICK SETUP")
    print("=" * 60)
    print("This downloads all model weights so alignment runs instantly.")
    print("Models:")
    print("  1. WhisperX large-v2  (~3 GB, one-time download)")
    print("  2. Wav2Vec2 aligner   (~300 MB, one-time download)")
    print()


def check():
    print("── Dependency Check ────────────────────────────────────")
    ok = True

    if shutil.which("ffmpeg"):
        print("[OK] ffmpeg found")
    else:
        print("[WARN] ffmpeg not found — WhisperX needs ffmpeg on PATH")
        ok = False

    try:
        import whisperx
        print("[OK] whisperx installed")
    except ImportError:
        print("[ERROR] whisperx not installed")
        print("        pip install git+https://github.com/m-bain/whisperX.git")
        ok = False

    try:
        import torch
        print(f"[OK] torch {torch.__version__}")
        if torch.cuda.is_available():
            print(f"[OK] CUDA — {torch.cuda.get_device_name(0)}")
        else:
            print("[WARN] CUDA not available — will use CPU (slower)")
    except ImportError:
        print("[ERROR] torch not installed")
        ok = False

    print()
    return ok


def download_models():
    import whisperx

    # ── Model 1: WhisperX large-v2 ──────────────────────────────
    print("── Step 1/2: WhisperX large-v2 ────────────────────────")
    print("  Downloading ~3 GB ... progress bars appear below:")
    t = time.time()
    try:
        whisperx.load_model("large-v2", device="cpu", compute_type="int8")
        print(f"  [OK] Done in {time.time()-t:.0f}s\n")
    except Exception as e:
        print(f"  [ERROR] {e}\n")
        return

    # ── Model 2: Wav2Vec2 aligner ────────────────────────────────
    print("── Step 2/2: Wav2Vec2 English Alignment Model ──────────")
    print("  Downloading ~300 MB ... progress bars appear below:")
    t = time.time()
    try:
        whisperx.load_align_model(language_code="en", device="cpu")
        print(f"  [OK] Done in {time.time()-t:.0f}s\n")
    except Exception as e:
        print(f"  [ERROR] {e}\n")
        return

    print("=" * 60)
    print("  SETUP COMPLETE — run test_alignment.py to align lyrics!")
    print("=" * 60)


if __name__ == "__main__":
    banner()
    if check():
        download_models()
    else:
        print("[SETUP ABORTED] Fix the errors above first.")
