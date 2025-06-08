# 🎵 Music Tools Suite

**Complete workflow: YouTube → MP3 → Stems → Player**

A streamlined single-file application that combines YouTube downloading, AI-powered stem separation, and professional mixing into one seamless workflow.

## ✨ Features

### 🎬 1. YouTube to MP3
- Download any YouTube video as high-quality MP3 (320kbps)
- Fast processing (10-30 seconds)
- Smart folder management with session persistence
- Direct download buttons

### 🎛️ 2. Separate MP3 to Stems  
- AI-powered stem separation using Meta's Demucs
- Individual tracks: vocals, drums, bass, other
- Process downloaded MP3 or upload existing files
- High-quality MP3 stem output

### 🎚️ 3. Play & Mix Stems
- Professional mixing interface with synchronized playback
- Individual volume, mute, and solo controls
- Master volume and progress controls
- Individual stem progress indicators
- Browser fullscreen mode
- **Full keyboard control support**

## ⌨️ Keyboard Controls

### 🎵 Playback
- `Spacebar` - Play/Pause
- `S` or `Esc` - Stop
- `F` - Toggle Fullscreen
- `M` - Master Mute/Unmute

### 🎚️ Navigation & Volume
- `↑/↓` - Master Volume ±5%
- `←/→` - Seek ±10 seconds

### 🎛️ Individual Stem Controls
- `1-9` - Solo/Unsolo stem (by position)
- `Shift+1-9` - Mute/Unmute stem

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (system dependency)
# macOS:
brew install ffmpeg

# Linux:
sudo apt install ffmpeg

# Windows:
# Download from https://ffmpeg.org/
```

### Run Application
```bash
streamlit run app.py
```

## 🔄 Complete Workflow

1. **YouTube → MP3**: Paste a YouTube URL and download as MP3
2. **MP3 → Stems**: Separate the downloaded MP3 (or upload existing) into individual instrument tracks
3. **Play & Mix**: Load stems into the professional player for mixing

## 💡 Smart Features

- **Folder Persistence**: Set a folder once, used throughout the session
- **Quick Actions**: Contextual prompts guide you to the next step
- **Session Memory**: Downloaded MP3s and separated stems are remembered
- **Auto-Loading**: Stems from separation automatically load into the player
- **Flexible Entry**: Jump in at any step with your own files

## 📁 File Structure

```
music-tools-suite/
├── app.py              # Complete single-page application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🎯 Use Cases

- **Music Production**: Isolate instruments for remixing
- **Karaoke Creation**: Remove vocals from songs
- **Educational**: Study individual instrument parts
- **Content Creation**: Create backing tracks and stems

## 🛠️ Technical Details

- **Frontend**: Streamlit with custom CSS styling
- **YouTube Download**: yt-dlp for reliable video processing
- **Stem Separation**: Meta's Demucs AI model
- **Audio Processing**: FFmpeg for format conversion
- **Playback**: HTML5 audio with JavaScript controls
- **Keyboard Controls**: Professional DAW-style shortcuts

## 📋 Requirements

- Python 3.8+
- Streamlit
- yt-dlp
- demucs
- soundfile
- torchaudio
- FFmpeg (system dependency)

## 🚧 Notes

- Stem separation is CPU-intensive and may take 2-10+ minutes depending on song length
- Ensure adequate disk space for processing temporary files
- For best performance, use modern multi-core CPU with 8GB+ RAM

---

**🎵 Enjoy creating with the Music Tools Suite!** 