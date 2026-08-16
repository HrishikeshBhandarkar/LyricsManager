# 🎵 LyricsManager

<div align="center">

```
█░░ █▄█ █▀█ █ █▀▀  █▀▄▀█ █▀█ █▄░█ █▀█ █▀▀ █▀▀ █▀█
█▄▄ ░█░ █▀▄ █ █▄▄  █░▀░█ █▀█ █░▀█ █▀█ █▄█ ██▄ █▀▄
```

**The Ultimate CLI & AI Engine for Millisecond-Precision Synced Lyrics (`.elrc` / `.lrc`)**

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Audio Formats](https://img.shields.io/badge/Audio%20Formats-M4A%20%7C%20MP3%20%7C%20FLAC%20%7C%20ALAC%20%7C%20AAC%20%7C%20WebM-green.svg)](#-supported-audio-formats)
[![Web Providers](https://img.shields.io/badge/Web%20Providers-7%20APIs-orange.svg)](#-7-multi-source-web-providers)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Demucs%20%2B%20WhisperX-purple.svg)](#-local-neural-ai-forced-aligner)

</div>

---

## ⚡ What is LyricsManager?

Ever wanted **Apple Music / Spotify-style glowing, word-by-word animated lyrics** for your local music collection?

Most lyric fetchers only download plain text or basic line-by-line `.lrc` files. **LyricsManager** brings true millisecond-accurate word-level synchronization to your audio library:

1. **Scrapes & Decrypts 7 Major Streaming APIs**: Pulls rich, syllable-synced lyrics from Apple Music, Musixmatch, QQ Music, NetEase, KuGou, and LRCLIB — automatically decrypting proprietary encrypted formats (TTML, QRC, KRC, YRC, RichSync).
2. **Local Neural AI Forced Alignment**: If a song doesn't have synced lyrics anywhere online, LyricsManager separates the vocals using **Demucs** and aligns every spoken syllable using **WhisperX + Wav2Vec2 CTC phoneme models**.
3. **Embeds Metadata Directly Into Your Tracks**: Automatically writes lyrics into ID3 (`USLT`), Vorbis Comments (`LYRICS`), and MP4 atoms (`©lyr`), plus exports standalone `.elrc` and `.lrc` sidecar files.
4. **Apple Music Web Player Included**: Comes with a gorgeous, fluid Now Playing web player (`AppleMusicLyrics/index.html`) featuring animated artwork canvas, dynamic palette ambient tinting, and real-time syllable karaoke animation.

---

## ✨ Features

- 🌐 **7 High-Precision Web Providers**: BiniLyrics (Apple Music TTML), QQ Music (QRC), NetEase (YRC), KuGou (KRC), Musixmatch (RichSync), Paxsenix, and LRCLIB.
- 🤖 **Neural AI Forced Alignment**: Isolate vocals with Demucs and generate word timestamps from scratch with WhisperX.
- 📂 **Universal Tag Embedding**: Writes synced lyrics directly into audio metadata tags so mobile players and desktop apps read them automatically.
- 💻 **Interactive Dropdown Shell**: Has an interactive shell for people who hate CLI (`/fetch`, `/ai`, `/scan`, `/config`, `/help`, `/exit`).
- 🎨 **Apple Music Player UI**: Pure client-side web player that reads your embedded tags and plays synced word-by-word animations smoothly.
- 🔄 **Smart Re-Fetch & Provider Priority**: Reject bad lyrics with one keystroke and re-query alternative APIs on the fly.

---

## 🚀 Quickstart

### 1. Installation
Clone the repository and install locally:
```bash
git clone https://github.com/HrishikeshBhandarkar/LyricsManager.git
cd LyricsManager
pip install -e .
```

*Optional: To enable local GPU/CPU neural AI alignment (Demucs + WhisperX):*
```bash
pip install -e .[ai]
```

### 2. Launch the Interactive Shell
Just run:
```bash
lyric_manager
```
This opens the interactive terminal shell with dropdown command autocompletion and sleek vector styling.

---

## 💻 CLI Commands

You can run commands directly from your terminal:

```bash
# Fetch lyrics for a song (auto-scrapes 7 providers)
lyric_manager fetch --title "Blinding Lights" --artist "The Weeknd"

# Fetch specifically from a provider alias (e.g. Apple Music / QQ Music / Musixmatch)
lyric_manager fetch --title "Starboy" --artist "The Weeknd" --provider bini

# Run AI forced alignment on a music folder
lyric_manager ai

# Configure AI model size and default provider priority
lyric_manager config
```

### Interactive Slash Commands
| Command | What It Does |
| :--- | :--- |
| **`/fetch`** | Search 7 web APIs interactively for any song |
| **`/ai`** | Scan an audio folder & run WhisperX + Demucs AI forced alignment |
| **`/scan`** | Batch scan an audio directory with instant re-fetching and tag embedding |
| **`/config`** | Configure AI model (`base` vs `large-v2`) and provider priorities |
| **`/help`** | View CLI help menu and provider matrix |
| **`/exit`** | Exit the shell |

---

## 🌐 7 Multi-Source Web Providers

| Alias | Provider | Precision | Details |
| :--- | :--- | :--- | :--- |
| **`bini`** | **BiniLyrics** | Word-by-Word | Apple Music TTML with syllable timestamps |
| **`qq`** | **QQ Music** | Word-by-Word | High-precision QRC lyrics with triple-DES decryption |
| **`netease`**| **NetEase Cloud Music** | Word-by-Word | Studio-grade YRC synced lyrics |
| **`kugou`** | **KuGou Music** | Word-by-Word | Dynamic KRC lyrics |
| **`mxm`** | **Musixmatch** | Word-by-Word | Official Musixmatch RichSync word alignments |
| **`pax`** | **Paxsenix** | Word & Line | Apple Music REST API integration |
| **`lrc`** | **LRCLIB** | Line & Plain | Open-source crowd-sourced synced fallback |

---

## 🤖 Local Neural AI Forced Aligner

When a track has zero synced lyrics online, LyricsManager's local AI engine takes over:

```
[Audio File] ──> [Demucs Neural Vocal Split] ──> [WhisperX VAD + ASR] ──> [Wav2Vec2 Phoneme CTC Align] ──> [Studio .elrc]
```

1. **Demucs Hybrid Transformer**: Strips heavy guitars, bass, and drums to isolate a crystal-clear 16kHz vocal stem.
2. **WhisperX VAD + ASR**: Detects exact vocal timestamps and transcribes words.
3. **Wav2Vec2 CTC Phoneme Alignment**: Aligns individual syllables against acoustic phoneme probabilities.
4. **Energy Interpolation**: Calibrates word boundaries to match vocal transients with millisecond precision.

---

## 🎨 Apple Music Web Player

LyricsManager includes a standalone Apple Music-styled lyrics player located in `AppleMusicLyrics/index.html`.

- **Side-by-Side Dual Column View**: Large album art on the left, fluid scrolling animated lyrics on the right.
- **Embedded Tag Reader**: Reads embedded lyrics and album art directly from your **M4A, MP3, FLAC, ALAC, AAC, WebM** files upon drop.
- **Dynamic Blurred Background**: Ambient lighting matches the exact color palette of your album art.
- **Interactive Scrubbing**: Click any line of lyrics to jump directly to that part of the song.

Simply open `AppleMusicLyrics/index.html` in Chrome/Edge/Firefox and drag in your audio files!

---

## 🏷️ Supported Audio Formats

| Format | Extension | Metadata Tag Used |
| :--- | :--- | :--- |
| **MPEG Audio** | `.mp3` | ID3v2 `USLT` frame |
| **MPEG-4 Audio** | `.m4a`, `.aac` | MP4 Atom `©lyr` |
| **Apple Lossless** | `.alac` | MP4 Atom `©lyr` |
| **Free Lossless Audio** | `.flac` | Vorbis Comment `LYRICS` |
| **WebM Audio** | `.webm` | Vorbis Comment `LYRICS` |

---

## 🗑️ Uninstallation

If you ever want to remove LyricsManager and clean up build artifacts or caches:

```bash
# Interactive uninstaller
python uninstall.py

# Or quick standard uninstall:
python uninstall.py -y
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
