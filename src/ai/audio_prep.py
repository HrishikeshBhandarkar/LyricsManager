"""
AUDIO PREPARATION MODULE
Simple, clean audio loading functions.
Demucs neural separation provides pristine vocal stems natively.
No artificial compression or aggressive filters that distort the spectrum.
"""
from pathlib import Path
import numpy as np

def clean_audio_pass(audio_np: np.ndarray) -> np.ndarray:
    """Returns clean float32 audio normalized to [-1.0, 1.0]."""
    audio = audio_np.astype(np.float32)
    peak = np.max(np.abs(audio)) + 1e-12
    if peak > 1.0:
        audio = audio / peak
    return audio
