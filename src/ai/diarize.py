import math
import re
import numpy as np
import torch
import os
import shutil
import pathlib
from difflib import SequenceMatcher

# Monkeypatch symlink to bypass Windows privilege error for HuggingFace caching
_original_symlink = pathlib.Path.symlink_to

def _mock_symlink(self, target, *args, **kwargs):
    try:
        shutil.copy(target, self)
    except Exception:
        _original_symlink(self, target, *args, **kwargs)

pathlib.Path.symlink_to = _mock_symlink

# NOTE: librosa is NOT used here. SpeechBrain 1.1.0 injects lazy-import
# placeholder modules (e.g. speechbrain.integrations.k2_fsa) into sys.modules.
# librosa's lazy_loader calls inspect.getmodule(), which iterates sys.modules
# and triggers the placeholder's __getattr__ -> tries to import uninstalled
# "k2" -> ImportError. soundfile + scipy avoid this entirely.
import soundfile as sf
from scipy.signal import resample_poly
from speechbrain.inference.speaker import EncoderClassifier


def load_audio_channels(audio_path: str, target_sr: int):
    """Read audio as (channels, samples) float32 at target_sr without librosa."""
    data, native_sr = sf.read(audio_path, dtype="float32", always_2d=True)
    if native_sr != target_sr:
        g = math.gcd(native_sr, target_sr)
        data = resample_poly(data, target_sr // g, native_sr // g, axis=0)
    return data.T, native_sr


def librosa_to_mono(y_stereo):
    """Channel-mean collapse matching librosa.to_mono behavior."""
    return y_stereo.mean(axis=0)


def _apply_overlap_speakers(lines_with_words, overlap_ratio: float = 0.35, match_ratio: float = 0.7):
    """
    Overlap-based v1/v2 assignment with the word-repeat twist.

    Rule: when two lines play at the same time for more than `overlap_ratio`
    (35%) of the EARLIER line's duration, they carry different lyrics sung
    simultaneously -> two different people -> assign them v1 + v2.

    Twist: when the later line's words repeat a word sequence a previously
    assigned line (v1 or v2) sang, the two singers' audio profiles overlap
    mathematically and embeddings cannot separate them — the text is the only
    reliable signal, so the later line inherits that same speaker.
    """

    def _norm(text: str) -> str:
        return re.sub(r"[^0-9a-z\u0900-\u097f ]", "", text.lower())

    history = []  # (speaker, normalized words) of finalized lines
    for i, ld in enumerate(lines_with_words):
        if "_start" not in ld:
            history.append((ld.get("speaker", "v1"), ""))
            continue
        s1, e1 = ld["_start"], ld["_end"]
        text_i = _norm(" ".join(w.get("word", "") for w in ld.get("words", [])))

        for j in range(i):  # the "previous" line in the song
            pj = lines_with_words[j]
            if "_start" not in pj:
                continue
            s2, e2 = pj["_start"], pj["_end"]
            dur_j = max(e2 - s2, 1e-6)
            overlap_dur = min(e1, e2) - max(s1, s2)
            if overlap_dur <= overlap_ratio * dur_j:
                continue  # under 35% of the previous line's life — not proof

            # ── Twist: repeated words -> same speaker as an earlier line ──
            best_spk, best_score = None, 0.0
            for spk, txt in history:
                if not txt:
                    continue
                score = 1.0 if (text_i in txt or txt in text_i) else SequenceMatcher(None, text_i, txt).ratio()
                if score > best_score:
                    best_score, best_spk = score, spk
            if best_spk is not None and best_score >= match_ratio:
                ld["speaker"] = best_spk
                continue

            # ── Different lyrics at the same time -> two different people ──
            other = pj.get("speaker", "v1")
            if ld.get("speaker", "v1") == other:
                ld["speaker"] = "v2" if other == "v1" else "v1"

        history.append((ld.get("speaker", "v1"), text_i))


def assign_speakers(vocal_audio_path: str, lines_with_words: list, sample_rate: int = 16000):
    if not lines_with_words:
        return lines_with_words
        
    print("    >> Loading SpeechBrain ECAPA-TDNN model...")
    # Reuse the stable cached model folder next to this script. Building savedir
    # from dirname(vocal_audio_path) is wrong: the vocal stem is stored in a
    # temporary "separated/" folder that gets deleted after each run, forcing
    # a fresh ~100MB HuggingFace re-download (or failure -> all-v1 fallback).
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "speechbrain_model")
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", 
        savedir=model_dir,
        run_opts={"device": "cuda" if torch.cuda.is_available() else "cpu"}
    )
    
    y_stereo, _ = load_audio_channels(vocal_audio_path, sample_rate)
    is_stereo = (y_stereo.ndim == 2 and y_stereo.shape[0] == 2)
    if is_stereo:
        y_mono = librosa_to_mono(y_stereo)
    else:
        y_mono = y_stereo.reshape(-1)
        
    sr = sample_rate
    features = []
    
    print("    >> Extracting Speaker Embeddings & Panning...")
    for i, line_data in enumerate(lines_with_words):
        words = line_data.get("words", [])
        if not words:
            continue
            
        start_time = words[0]["start"]
        end_time = words[-1]["end"]
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        if end_sample <= start_sample:
            end_sample = start_sample + 1024
            
        segment_mono = y_mono[start_sample:end_sample]
        min_len = int(1.0 * sr)
        if len(segment_mono) < min_len:
            segment_mono = np.pad(segment_mono, (0, min_len - len(segment_mono)))
            
        signal = torch.from_numpy(segment_mono).unsqueeze(0).to(classifier.device)
        with torch.no_grad():
            emb = classifier.encode_batch(signal)
            
        emb_vec = emb.squeeze().cpu().numpy()
        
        pan_bias = 0.0
        if is_stereo:
            seg_L = y_stereo[0, start_sample:end_sample]
            seg_R = y_stereo[1, start_sample:end_sample]
            energy_L = np.sum(seg_L ** 2)
            energy_R = np.sum(seg_R ** 2)
            total_energy = energy_L + energy_R
            if total_energy > 0:
                pan_bias = (energy_R - energy_L) / total_energy
        
        pan_feature = np.array([pan_bias * 1.2]) 
        norm = np.linalg.norm(emb_vec)
        if norm > 0:
            emb_vec = emb_vec / norm
            
        combined_vec = np.concatenate([emb_vec, pan_feature])
        norm2 = np.linalg.norm(combined_vec)
        if norm2 > 0:
            combined_vec = combined_vec / norm2
            
        features.append(combined_vec)
        line_data["_emb"] = combined_vec
        line_data["_start"] = start_time
        line_data["_end"] = end_time
        
    if len(features) < 2:
        for line in lines_with_words:
            line["speaker"] = "v1"
        return lines_with_words

    # --- TWO-CLUSTER SPEAKER ASSIGNMENT (replaces fragile single-anchor
    #     threshold which mislabeled everything when same-speaker cosine
    #     similarity on singing vocals is well below 0.5) ---
    # Spherical k-means (k=2) over the L2-normalized embeddings. The cluster
    # containing the first sung line becomes V1, the other becomes V2.
    emb_matrix = np.stack(features)                    # (n_lines, d), L2 normalized

    v1_profile = emb_matrix[0].copy()                  # first-line cluster seed
    sims_to_seed = emb_matrix @ v1_profile
    v2_profile = emb_matrix[int(np.argmin(sims_to_seed))].copy()

    cluster_of_line = np.zeros(len(emb_matrix), dtype=int)
    for _ in range(50):
        sim_v1 = emb_matrix @ v1_profile
        sim_v2 = emb_matrix @ v2_profile
        new_cluster = np.where(sim_v1 >= sim_v2, 0, 1)
        if np.array_equal(new_cluster, cluster_of_line):
            break
        cluster_of_line = new_cluster
        for c in (0, 1):
            mask = cluster_of_line == c
            if mask.any():
                centroid = emb_matrix[mask].mean(axis=0)
                norm = np.linalg.norm(centroid)
                if norm > 0:
                    centroid = centroid / norm
                if c == 0:
                    v1_profile = centroid
                else:
                    v2_profile = centroid

    # Guards: collapse to a single speaker only when the two clusters are 
    # essentially the identical voice (highly correlated embeddings).
    # Removed the strict "small_cluster < 10%" check so a guest artist singing 
    # just 1 line is still correctly labeled as V2!
    centroid_sim = float(v1_profile @ v2_profile)
    single_speaker = (centroid_sim > 0.85)

    if single_speaker:
        for line in lines_with_words:
            line["speaker"] = "v1"
    else:
        # Map the cluster that holds the first sung line to V1.
        first_cluster = cluster_of_line[0]
        cluster_to_speaker = {first_cluster: "v1", 1 - first_cluster: "v2"}
        line_emb_idx = 0
        for line_data in lines_with_words:
            if "_emb" in line_data:
                line_data["speaker"] = cluster_to_speaker[cluster_of_line[line_emb_idx]]
                line_emb_idx += 1

    # Overlap -> v1/v2 assignment (35% rule + word-repeat twist)
    _apply_overlap_speakers(lines_with_words)

    for line_data in lines_with_words:
        if "speaker" not in line_data:
            line_data["speaker"] = "v1"
        line_data.pop("_emb", None)
        line_data.pop("_start", None)
        line_data.pop("_end", None)

    return lines_with_words
