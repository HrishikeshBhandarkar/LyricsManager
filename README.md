# 🎵 LyricsManager

<div align="center">

```
█░░ █▄█ █▀█ █ █▀▀  █▀▄▀█ █▀█ █▄░█ █▀█ █▀▀ █▀▀ █▀█
█▄▄ ░█░ █▀▄ █ █▄▄  █░▀░█ █▀█ █░▀█ █▀█ █▄█ ██▄ █▀▄
```

**The Ultimate CLI & AI Engine for Millisecond-Precision Synchronized Lyrics (`.elrc` / `.lrc`)**

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Supported Audio Formats](https://img.shields.io/badge/Audio%20Formats-127%2B-green.svg)](#-universal-audio-format-support-127-extensions)
[![Web Providers](https://img.shields.io/badge/Web%20Providers-7%20APIs-orange.svg)](#-7-multi-source-web-lyric-providers)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Demucs%20%2B%20WhisperX-purple.svg)](#-hybrid-ai-forced-alignment-pipeline)

</div>

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Pipeline](#-architecture--pipeline)
- [7 Multi-Source Web Lyric Providers](#-7-multi-source-web-lyric-providers)
- [Universal Audio Format Support (127+ Extensions)](#-universal-audio-format-support-127-extensions)
- [Installation & Setup](#-installation--setup)
- [Interactive Shell Guide](#-interactive-shell-guide)
- [CLI Command Reference](#-cli-command-reference)
- [Configuration & Settings (`config.json`)](#-configuration--settings-configjson)
- [Metadata Tag Embedding & Exporting](#-metadata-tag-embedding--exporting)
- [Dependency & Consent Management](#-dependency--consent-management)
- [Language Compatibility Notes](#-language-compatibility-notes)
- [License](#-license)

---

## 🌟 Overview

**LyricsManager** is a high-performance terminal tool designed to automate fetching, generating, and embedding synchronized lyrics into your local audio collection.

Whether you need **word-by-word animated lyrics (`.elrc`)** matching Apple Music / Spotify standards or **standard line-by-line synced lyrics (`.lrc`)**, LyricsManager bridges the gap between global streaming APIs and local neural AI forced alignment:

1. **Scrapes 7 Major Web Lyric Providers** with decryption for proprietary encrypted formats (TTML, QRC, KRC, YRC, RichSync).
2. **AI Forced Alignment Engine** that separates vocals using **Demucs** and aligns word timestamps using **WhisperX + Wav2Vec2 CTC** phoneme models.
3. **Recursive Directory Scanner** that mass-processes entire music folders across **127 audio formats** with live progress bars, engaging trivia tickers, and batch summary panels.
4. **Direct Audio Tag Embedding** into ID3 (MP3), Vorbis Comments (FLAC, OGG, Opus), and MP4 atoms (M4A, AAC, ALAC).

---

## ✨ Key Features

- **⚡ Interactive Terminal Shell**: Dropdown auto-complete, command suggestions, and Rich vector styling (`/fetch`, `/ai`, `/scan`, `/config`, `/help`, `/exit`).
- **🌐 7 High-Precision Web APIs**: Connects to BiniLyrics (Apple Music), QQ Music, NetEase Cloud Music, KuGou Music, Musixmatch, Paxsenix, and LRCLIB.
- **🤖 Demucs + WhisperX Neural Alignment**: Generates word timestamps from scratch using local GPU/CPU neural models if web sources lack synced data.
- **📂 127 Audio File Formats Supported**: Scans and parses metadata from every consumer, lossless, audiophile, broadcast, tracker, and retro chiptune audio format.
- **🔄 Smart Re-Fetch & Provider Priority**: Set your favorite provider in configuration, or easily reject unsatisfactory lyrics and re-query alternative APIs during scanning.
- **🧠 Automatic VRAM Management**: Automatically unloads heavy AI models and flushes CUDA/CPU memory immediately after batch alignment jobs finish.
- **🔒 Consent-First Dependency Management**: Checks dependencies on startup and requests explicit user permission before installing packages via pip.

---

## 🏗️ Architecture & Pipeline

```
                                  ┌────────────────────────┐
                                  │   Local Audio File     │
                                  │ (127 Supported Formats)│
                                  └───────────┬────────────┘
                                              │
                                   [Scanner & Metadata]
                                              │
                    ┌─────────────────────────┴────────────────────────┐
                    ▼                                                  ▼
       ┌─────────────────────────┐                        ┌─────────────────────────┐
       │   7 Web API Providers   │                        │   AI Alignment Engine   │
       │                         │                        │                         │
       │ • BiniLyrics (TTML)     │                        │ 1. FFmpeg 16kHz Mono    │
       │ • QQ Music (QRC)        │                        │ 2. Demucs Vocal Split   │
       │ • NetEase (YRC)         │                        │ 3. WhisperX VAD + ASR   │
       │ • KuGou (KRC)           │                        │ 4. Wav2Vec2 CTC Align   │
       │ • Musixmatch (RichSync) │                        │ 5. DTW Forward Match    │
       │ • Paxsenix (Apple API)  │                        │ 6. Energy Interpolation │
       │ • LRCLIB (LRC / Plain)  │                        └────────────┬────────────┘
       └────────────┬────────────┘                                     │
                    │                                                  │
                    └─────────────────────────┬────────────────────────┘
                                              ▼
                                 ┌─────────────────────────┐
                                 │   Reference ELRC / LRC  │
                                 │   Timestamp Formatter   │
                                 └────────────┬────────────┘
                                              │
                    ┌─────────────────────────┴────────────────────────┐
                    ▼                                                  ▼
       ┌─────────────────────────┐                        ┌─────────────────────────┐
       │   Sidecar File Export   │                        │  Metadata Tag Embedding │
       │                         │                        │                         │
       │   Artist - Title.elrc   │                        │ • ID3v2 USLT (MP3)      │
       │   Artist - Title.lrc    │                        │ • Vorbis LYRICS (FLAC)  │
       │                         │                        │ • MP4 ©lyr Atom (M4A)   │
       └─────────────────────────┘                        └─────────────────────────┘
```

---

## 🌐 7 Multi-Source Web Lyric Providers

| Alias | Provider Name | Default Precision | Encryption / Format Decoded |
| :---: | :--- | :---: | :--- |
| **`bini`** | **BiniLyrics (Apple Music)** | Word-by-Word | XML TTML with vocal roles (`v1`, `v2`, `[bg:]`) |
| **`qq`** | **QQ Music** | Word-by-Word | QRC encrypted XML (3-decimal millisecond timestamps) |
| **`netease`**| **NetEase Cloud Music** | Word-by-Word | YRC line + intra-word relative timestamps |
| **`kugou`** | **KuGou Music** | Word-by-Word | KRC 16-byte cyclic XOR decryption + zlib decompression |
| **`mxm`** | **Musixmatch** | Word-by-Word | RichSync syllable-level offsets |
| **`pax`** | **Paxsenix (Apple Music API)**| Word-by-Word | REST JSON payload parser with iTunes ID resolution |
| **`lrc`** | **LRCLIB** | Line-Synced | Open-source community database fallback |

---

## 📁 Universal Audio Format Support (127 Extensions)

Lyric Manager recursively scans and extracts metadata from **all audio formats on Earth**:

- **Consumer & Streaming**: `.mp3`, `.mp2`, `.mp1`, `.mpa`, `.m4a`, `.m4b`, `.m4p`, `.m4r`, `.aac`, `.mp4`, `.3gp`, `.3g2`, `.mov`
- **Lossless & Audiophile PCM**: `.flac`, `.fla`, `.wav`, `.wave`, `.bwf`, `.aiff`, `.aif`, `.aifc`, `.alac`, `.ape`, `.mac`, `.wv`, `.wvp`, `.tta`, `.tak`, `.ofr`, `.ofs`, `.shn`, `.dsd`, `.dsf`, `.dff`
- **Open Codecs**: `.ogg`, `.oga`, `.opus`, `.spx`, `.ogx`
- **Windows Media**: `.wma`, `.asf`
- **Cinema, Dolby & Multi-Channel**: `.ac3`, `.eac3`, `.ec3`, `.dts`, `.dtshd`, `.dtsma`, `.mlp`, `.truehd`, `.thd`
- **Speech & Mobile**: `.amr`, `.awb`, `.gsm`, `.qcp`, `.vox`
- **Studio, Legacy & Workstation**: `.au`, `.snd`, `.caf`, `.w64`, `.rf64`, `.pcm`, `.raw`, `.lpcm`, `.voc`, `.smp`, `.sd2`, `.iff`, `.svx`, `.8svx`, `.16sv`, `.paf`, `.sf`, `.nist`, `.sph`, `.avr`, `.cdr`, `.cda`
- **RealAudio & TwinVQ**: `.ra`, `.ram`, `.rm`, `.vqf`
- **Containers & Stems**: `.mka`, `.webm`, `.weba`, `.flv`, `.f4a`, `.f4b`
- **MIDI & Tracker Formats**: `.mid`, `.midi`, `.kar`, `.rmi`, `.mod`, `.xm`, `.it`, `.s3m`, `.stm`, `.mtm`, `.umx`, `.mo3`, `.669`, `.far`, `.okt`, `.ptm`
- **Chiptune & Video Game Audio**: `.vgm`, `.vgz`, `.nsf`, `.nsfe`, `.spc`, `.gym`, `.gbs`, `.hes`, `.kss`, `.ay`, `.sap`, `.sid`
- **Game Engine Formats**: `.adx`, `.hca`, `.brstm`, `.bcstm`, `.bfstm`, `.vag`, `.at9`, `.at3`, `.xma`, `.fsb`, `.bnk`, `.pck`

---

## 🚀 Installation & Setup

### 1. Prerequisites
- **Python 3.10, 3.11, or 3.12**
- **FFmpeg** installed and added to your system `PATH` (required for audio decoding and AI stem separation).

### 2. Standard Installation (Web API Lyric Fetching)
Clone the repository and install standard requirements:
```bash
git clone https://github.com/HrishikeshBhandarkar/LyricsManager.git
cd LyricsManager
pip install -e .
```

### 3. Full AI Installation (WhisperX & Demucs Vocal Isolation)
To enable local AI forced alignment with GPU acceleration:
```bash
pip install -e .[ai]
```

---

## 💻 Interactive Shell Guide

Simply launch `lyric_manager` without flags to enter the interactive shell:
```bash
lyric_manager
```

### Interactive Slash Commands
| Command | Action |
| :--- | :--- |
| **`/fetch`** | Search 7 web APIs interactively for a single song |
| **`/ai`** | Scan a directory and run WhisperX forced alignment on selected tracks |
| **`/scan`** | Scan an audio directory with batch re-fetching and embedding |
| **`/config`** | Configure AI model size (`base` vs `large-v2`) and preferred provider |
| **`/help`** | Display the master CLI help menu and provider matrix |
| **`/help <cmd>`** | Display dedicated help for a specific command (e.g. `/help fetch`, `/help ai`) |
| **`/exit`** | Exit the interactive shell |

---

## ⚡ CLI Command Reference

### 1. Web Fetch (`lyric_manager fetch`)
Search and retrieve synchronized lyrics from online providers.
```bash
# Basic fetch (prompts if arguments are missing)
lyric_manager fetch --title "Starboy" --artist "The Weeknd"

# Fetch line-synced lyrics only
lyric_manager fetch --title "Sanam Re" --artist "Mithoon" --format LRC

# Query a specific provider directly (bypassing smart auto-routing)
lyric_manager fetch --title "Pungi" --artist "Pritam" --provider qq --format ELRC
```

### 2. AI Forced Alignment (`lyric_manager ai`)
Isolate vocals and generate millisecond-accurate word timestamps using local neural models.
```bash
# Auto-fetch official transcript from LRCLIB and align audio
lyric_manager ai --audio "./song.flac" --format ELRC

# Align audio against your own local lyrics transcript
lyric_manager ai --audio "./song.mp3" --transcript "./lyrics.txt" --format ELRC
```

### 3. Settings Configuration (`lyric_manager config`)
Launch the interactive configuration wizard:
```bash
lyric_manager config
```
- **[1] AI Model Size**:
  - `Base (Recommended)`: Blazing fast inference, lightweight VRAM footprint.
  - `Large-V2`: Recommended for very precise word stamps; higher VRAM usage.
- **[2] Top Preferred Provider**: Set a single top-priority API source (`bini`, `qq`, `netease`, `kugou`, `mxm`, `pax`, `lrc`, or `none`).
- **[3] Full Custom Fallback Chain**: Define the exact sequence and fallback chain (e.g. `qq, netease, kugou, bini, mxm, lrc, pax`) that completely overrides hardcoded search logic.

---

## ⚙️ Configuration & Settings (`config.json`)

Settings are stored in `config.json` in the root directory:
```json
{
    "whisper_model": "base",
    "preferred_provider": "qq",
    "provider_order": [
        "qq",
        "netease",
        "kugou",
        "bini",
        "mxm",
        "lrc",
        "pax"
    ]
}
```

---

## 🏷️ Metadata Tag Embedding & Exporting

When saving lyrics, Lyric Manager provides three options:
1. **Embed into Audio File**: Writes tags directly to audio files using Mutagen (`USLT` for MP3, `LYRICS` for FLAC/OGG, `©lyr` for M4A/AAC).
2. **Save as Sidecar File**: Saves standalone `.elrc` (word-by-word) or `.lrc` (line-by-line) files next to the audio file named `Artist - Title.elrc`.
3. **Both (Recommended)**: Embeds metadata into the audio file AND exports a clean sidecar file for external music players.

---

## 🛡️ Dependency & Consent Management

Lyric Manager includes a **consent-first dependency router** in `dependencies.py`:
- **First Run Check**: On initial startup, core libraries (`rich`, `prompt_toolkit`, `click`, `mutagen`, `requests`, `syncedlyrics`) are verified. If any are missing, the user is prompted for consent before downloading via pip.
- **AI Engine Isolation**: Heavy neural network dependencies (PyTorch, WhisperX, Demucs) are not forced on basic users. When entering AI mode, the tool asks for user permission before installing deep learning packages.

---

## 🌍 Language Compatibility Notes

- **English Audio**: Fully optimized. Produces studio-grade word-by-word alignments across diverse genres.
- **Hindi / Bollywood Audio**: Supported via built-in Devanagari normalization & Romanization in `ai/romanize.py`.
- **Other Languages**: WhisperX includes multilingual support across 99+ languages; however, accuracy on non-English singing audio can be hit-or-miss depending on vocal mixing, background instrumentation, and vocal styling. We recommend prioritizing native web providers (`qq`, `netease`, `kugou`, `bini`) for Asian and global tracks.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
