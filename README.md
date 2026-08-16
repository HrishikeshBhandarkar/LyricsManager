# LyricsManager

**A CLI and AI pipeline for fetching, decrypting, and generating millisecond-accurate, word-synced lyrics (`.elrc` / `.lrc`) for your local music library.**

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/HrishikeshBhandarkar/LyricsManager/blob/main/LICENSE)
[![Audio Formats](https://img.shields.io/badge/Audio%20Formats-M4A%20%7C%20MP3%20%7C%20FLAC%20%7C%20ALAC%20%7C%20AAC%20%7C%20WebM-green.svg)](#supported-audio-formats)
[![Web Providers](https://img.shields.io/badge/Web%20Providers-7%20APIs-orange.svg)](#multi-source-web-providers)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Demucs%20%2B%20WhisperX-purple.svg)](#local-neural-ai-forced-aligner)

> **Status:** actively developed — core fetching and tagging are stable; expect occasional rough edges around AI alignment and newer providers.

---

## What is LyricsManager?

Most lyric fetchers give you plain text or, at best, line-by-line `.lrc` timing. LyricsManager goes a step further: it pulls **word-level synced lyrics** — the kind that power the karaoke-style animations in Apple Music — and gets them onto your own files.

It does this in three ways:

1. **Scrapes and decrypts 7 streaming lyric APIs** — Apple Music, Musixmatch, QQ Music, NetEase, KuGou, and LRCLIB — handling each provider's proprietary format (TTML, QRC, KRC, YRC, RichSync) and any encryption they use along the way.
2. **Falls back to local AI alignment** when a song has no synced lyrics anywhere online: it isolates vocals with **Demucs** and aligns them syllable-by-syllable using **WhisperX** and a **Wav2Vec2 CTC** phoneme model.
3. **Writes the result directly into your files** — ID3 `USLT` frames, Vorbis `LYRICS` comments, and MP4 `©lyr` atoms — plus exports standalone `.elrc` / `.lrc` sidecar files.

A bundled web player (`AppleMusicLyrics/index.html`) lets you preview the synced lyrics with the same animated, Apple Music–style presentation.

---

## Features

- **7 web providers** — BiniLyrics (Apple Music TTML), QQ Music (QRC), NetEase (YRC), KuGou (KRC), Musixmatch (RichSync), Paxsenix, and LRCLIB, each with automatic decryption/parsing.
- **Neural forced alignment** — Demucs vocal isolation + WhisperX transcription for tracks with no lyrics available online.
- **Universal tag embedding** — writes synced lyrics into standard audio metadata so most desktop and mobile players pick them up automatically.
- **Interactive shell** — a slash-command interface (`/fetch`, `/ai`, `/scan`, `/config`, `/help`, `/exit`) for anyone who'd rather not memorize CLI flags.
- **Apple Music–style web player** — a client-side player that reads your embedded tags and renders word-by-word animated lyrics.
- **Smart re-fetch** — reject a bad match with one keystroke and immediately query the next provider in priority order.

---

## Quickstart

### 1. Install

```bash
git clone https://github.com/HrishikeshBhandarkar/LyricsManager.git
cd LyricsManager
pip install -e .
```

To enable local AI forced alignment (Demucs + WhisperX), also install the optional extras:

```bash
pip install -e .[ai]
```

### 2. Launch the interactive shell

```bash
lyric_manager
```

This opens the shell with command autocompletion, where you can fetch, scan, and configure without leaving the prompt.

---

## CLI Commands

You can also run everything directly from your terminal without the shell:

```bash
# Fetch lyrics for a song (queries all 7 providers)
lyric_manager fetch --title "Blinding Lights" --artist "The Weeknd"

# Fetch from a specific provider
lyric_manager fetch --title "Starboy" --artist "The Weeknd" --provider bini

# Run AI forced alignment on a folder of audio files
lyric_manager ai

# Configure AI model size and provider priority
lyric_manager config
```

### Interactive shell commands

| Command | Description |
|---|---|
| `/fetch` | Search all 7 web providers interactively for a song |
| `/ai` | Scan an audio folder and run Demucs + WhisperX forced alignment |
| `/scan` | Batch-scan a directory, with instant re-fetch and tag embedding |
| `/config` | Set AI model size (`base` vs `large-v2`) and provider priority |
| `/help` | Show the CLI help menu and provider matrix |
| `/exit` | Exit the shell |

---

## Multi-Source Web Providers

| Alias | Provider | Precision | Notes |
|---|---|---|---|
| `bini` | BiniLyrics | Word-by-word | Apple Music TTML with syllable timestamps |
| `qq` | QQ Music | Word-by-word | QRC lyrics, requires reproducing QQ's nonstandard DES variant to decrypt |
| `netease` | NetEase Cloud Music | Word-by-word | YRC synced lyrics |
| `kugou` | KuGou Music | Word-by-word | KRC lyrics |
| `mxm` | Musixmatch | Word-by-word | Official RichSync word alignments |
| `pax` | Paxsenix | Word & line | Apple Music REST API integration |
| `lrc` | LRCLIB | Line & plain | Open-source, crowd-sourced fallback |

---

## Local Neural AI Forced Aligner

When a track has no synced lyrics available from any provider, LyricsManager falls back to a local alignment pipeline:

```
[Audio File] → [Demucs vocal isolation] → [WhisperX VAD + ASR] → [Wav2Vec2 CTC phoneme alignment] → [.elrc output]
```

1. **Demucs** strips instrumentation to isolate a clean vocal stem.
2. **WhisperX** detects vocal activity and transcribes the words.
3. **Wav2Vec2 CTC** aligns individual syllables against phoneme probabilities.
4. Word boundaries are calibrated against vocal transients for millisecond-level accuracy.

This is slower than the API path and needs a reasonably capable CPU or GPU, but it means no song is ever left without synced lyrics.

---

## Apple Music Web Player

A standalone lyrics player ships in `AppleMusicLyrics/index.html`:

- Side-by-side layout — album art on one side, animated scrolling lyrics on the other.
- Reads embedded lyrics and artwork directly from dropped audio files (M4A, MP3, FLAC, ALAC, AAC, WebM).
- Ambient background tinting matched to the album art's color palette.
- Click any lyric line to jump to that point in the track.

Open the file directly in Chrome, Edge, or Firefox and drag in an audio file to try it.

---

## Supported Audio Formats

| Format | Extension | Metadata Tag |
|---|---|---|
| MPEG Audio | `.mp3` | ID3v2 `USLT` |
| MPEG-4 Audio | `.m4a`, `.aac` | MP4 atom `©lyr` |
| Apple Lossless | `.alac` | MP4 atom `©lyr` |
| FLAC | `.flac` | Vorbis comment `LYRICS` |
| WebM Audio | `.webm` | Vorbis comment `LYRICS` |

---

## Uninstalling

```bash
# Interactive uninstaller
python uninstall.py

# Or skip the prompts
python uninstall.py -y
```

---

## License

Distributed under the MIT License. See [LICENSE](https://github.com/HrishikeshBhandarkar/LyricsManager/blob/main/LICENSE) for details.
