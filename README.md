# LyricsManager

**LyricsManager** is a terminal-based Python CLI tool currently under **active development**, designed to streamline how synced lyrics are fetched, generated, and paired with local music libraries.

The project focuses on bringing high-precision, word-and-syllable-level timing directly to local media workflows—all executed through a lightweight, command-line interface.

> 🚧 **Project Status:** *Work in Progress.* Core modules for automated metadata extraction, API fetching, precision timestamp parsing, and AI-powered synchronization are actively being built and refined. Still not functional and in development

---

### ✨ Core Focus & Features

* 🖥️ **Terminal-First Workflow:** Built for the command line with zero heavy GUI overhead or bloat.
* 🎵 **Automated Audio Inspection:** Reads embedded tags directly from local `.mp3` and `.flac` files to handle track identification without manual user input.
* 🤖 **AI-Powered Local Syncing:** Integrates local AI models to process and generate word-level timestamped `.elrc` files directly on device, providing reliable fallbacks when online sources fall short.
* 🌐 **Multi-Source Fetching:** Connects to multiple external lyric providers and APIs to search, aggregate, and retrieve word-by-word synced data.
* ⏱️ **Precision Timestamping:** Focuses on extracting and structuring fine-grained word/syllable timing for enhanced lyric display engines.
* 📁 **Stateless & File-Based:** Operates completely on your local filesystem—simple, private, and requiring no external database or server overhead.
