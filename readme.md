# 🎵 VIAMP (VIAMP Is A Music Player)

**Fast. Minimal. Open-Source.**

VIAMP is a high-performance Windows music player that streams everything from the web without the bloat. Built for power users who want a beautiful interface and perfectly synced lyrics without the weight of a browser-based app.

!VIAMP Preview

## 🚀 Features

- **⚡ Instant Playback:** Powered by `yt-dlp` for lightning-fast streaming and minimal buffering.
- **🎤 Synced Lyrics:** Real-time, karaoke-style lyrics fetched automatically via `LRCLIB`.
- **💎 Modern UI:** A gorgeous, customizable dark-themed GUI built with Flet (Flutter for Python).
- **📦 Portable:** Packaged into a single `.exe`—no installation or Python required.
- **🔥 Lightweight:** Significantly lower RAM usage compared to Spotify or YouTube Music.

## 🛠️ Tech Stack

- **Frontend:** Flet (Flutter for Python)
- **Backend Engine:** yt-dlp
- **Lyrics API:** LRCLIB
- **Packaging:** PyInstaller

## 💻 Getting Started

### 🛠 Installation

**For Developers:**
```bash
# Clone the repo
git clone https://github.com/yourusername/VIAMP.git
cd VIAMP

# Install dependencies
pip install flet yt-dlp requests 

# Run the app
python main.py