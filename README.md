# 🎵 Music Tools Suite

**Complete workflow: YouTube → MP3 → Stems → Professional Mixing**

A streamlined single-page application that combines YouTube downloading, AI-powered stem separation, and professional mixing into one seamless workflow. Now with **one-click installation** for maximum ease of use!

## ✨ Core Features

### 🎬 YouTube to MP3
- Download any YouTube video as high-quality MP3 (320kbps)
- Lightning-fast processing (10-30 seconds)
- Smart folder management with session persistence
- Direct download buttons for local storage

### 🎛️ AI Stem Separation  
- Powered by **Meta's Demucs** - cutting-edge AI model
- Individual tracks: **vocals, drums, bass, other**
- Process downloaded MP3 or upload existing files
- Professional-quality MP3 stem output

### 🎚️ Professional Mixing Interface
- **Synchronized playback** across all stems
- Individual volume, mute, and solo controls
- Master volume and seek controls
- Individual stem progress indicators
- Browser fullscreen mode
- **Complete keyboard control** for professional workflow

## 🚀 Installation Options

Choose the method that works best for you:

### 🐍 Option 1: Python One-Click Installer (Recommended)
**Perfect for most users - handles everything automatically**

1. **Download** the Python installer package
2. **Run the installer**:
   ```bash
   python install.py
   ```
3. **Launch the app**:
   - Windows: Double-click `launch_music_tools.bat`
   - Mac/Linux: Run `./launch_music_tools.sh`

**✅ Handles**: Virtual environment, dependencies, FFmpeg installation, launchers

### 🐳 Option 2: Docker (Most Reliable)
**Guaranteed compatibility - works everywhere Docker runs**

1. **Download** the Docker package
2. **Run the launcher**:
   - Windows: Double-click `start_docker.bat`
   - Mac/Linux: Run `./start_docker.sh`

**✅ Handles**: All dependencies, isolation, auto-restart

### 💻 Option 3: Manual Development Setup
**For developers and customization**

```bash
# Clone/download the repository
git clone [repository-url]
cd music-tools-suite

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (system dependency)
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
# Windows: Download from https://ffmpeg.org/

# Run the application
streamlit run app.py
```

📖 **Detailed installation instructions**: See [`INSTALLATION.md`](INSTALLATION.md)

## ⌨️ Professional Keyboard Controls

### 🎵 Playback Controls
- `Spacebar` - Play/Pause all stems
- `S` or `Esc` - Stop playback
- `F` - Toggle browser fullscreen
- `M` - Master mute/unmute

### 🎚️ Navigation & Volume
- `↑/↓` - Master volume ±5%
- `←/→` - Seek ±10 seconds

### 🎛️ Individual Stem Controls
- `1-9` - Solo/unsolo stem by position
- `Shift+1-9` - Mute/unmute individual stems

**💡 Pro tip**: Click the player area first to activate keyboard shortcuts

## 🔄 Complete Workflow

### Linear Workflow (Recommended):
1. **YouTube → MP3**: Paste any YouTube URL and download as high-quality MP3
2. **MP3 → Stems**: Separate into individual instrument tracks using AI
3. **Mix & Play**: Professional mixing interface with all stems synchronized

### Flexible Entry Points:
- Start with **existing MP3 files** (skip download step)
- Upload **pre-separated stems** (skip separation step)
- **Jump between tools** as needed with persistent session data

## 💡 Smart Features

- **🔄 Folder Consistency**: Set a folder once, used throughout your session
- **⚡ Quick Actions**: Contextual prompts guide you to the next logical step
- **💾 Session Memory**: Downloaded MP3s and separated stems are remembered
- **🎯 Auto-Loading**: Stems from separation automatically load into the mixer
- **📱 Responsive Design**: Works on desktop and mobile browsers
- **🌐 Cross-Platform**: Windows, Mac, Linux support

## �� Project Structure

```
music-tools-suite/
├── 🎵 Core Application
│   ├── app.py                    # Complete single-page application (1,133 lines)
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # This documentation
│
├── 🛠️ Installation & Distribution
│   ├── install.py                # One-click Python installer
│   ├── Dockerfile                # Docker containerization
│   ├── docker-compose.yml        # Docker orchestration
│   ├── start_docker.sh           # Docker launcher (Unix)
│   ├── start_docker.bat          # Docker launcher (Windows)
│   └── create_distribution.sh    # Package creator for releases
│
└── 📖 Documentation
    ├── INSTALLATION.md           # User installation guide
    └── DISTRIBUTION.md           # Distribution strategy guide
```

## 🎯 Use Cases

### 🎼 Music Production
- **Remixing**: Isolate instruments for creative rearrangement
- **Sampling**: Extract clean drum loops, bass lines, vocals
- **Mashups**: Combine elements from multiple songs

### 🎤 Content Creation
- **Karaoke**: Remove vocals for sing-along tracks
- **Backing Tracks**: Create instrumental versions
- **Educational**: Study individual instrument parts and arrangements

### 🎧 Audio Analysis
- **Sound Design**: Analyze production techniques
- **Mixing Reference**: Compare individual elements across songs
- **Learning**: Understand how professional tracks are constructed

## 🛠️ Technical Architecture

### 🧠 AI & Processing
- **Stem Separation**: Meta's Demucs v4 (state-of-the-art neural network)
- **Audio Processing**: FFmpeg for format conversion and optimization
- **Download Engine**: yt-dlp for reliable YouTube processing

### 🖥️ Interface & UX
- **Frontend**: Streamlit with custom CSS for professional appearance
- **Audio Playback**: HTML5 with JavaScript for frame-perfect synchronization
- **Keyboard Controls**: DAW-style shortcuts for professional workflow
- **Responsive Design**: Works seamlessly across devices

### 🔧 Infrastructure
- **Cross-Platform**: Python-based for universal compatibility
- **Containerized**: Docker support for consistent deployment
- **Session Management**: Persistent state across workflow steps
- **Error Handling**: Comprehensive validation and user feedback

## 📋 System Requirements

### Minimum Requirements:
- **CPU**: Multi-core processor (stem separation is CPU-intensive)
- **RAM**: 4GB (8GB+ recommended for optimal performance)
- **Storage**: 2GB free space (for models, temporary files, output)
- **Internet**: Required for YouTube downloads and initial AI model download
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Recommended Configuration:
- **CPU**: Intel i5/AMD Ryzen 5 or better
- **RAM**: 8GB+ for smooth stem separation
- **Storage**: SSD for faster processing
- **Network**: Stable broadband for reliable downloads

## 🚧 Performance Notes

- **First Run**: Initial setup downloads ~2GB of AI models (one-time only)
- **Stem Separation**: Processing time varies by song length (2-10+ minutes)
- **Memory Usage**: Peaks during stem separation, minimal during playback
- **Disk Space**: Temporary files are cleaned up automatically
- **Optimization**: Close other resource-intensive applications for best performance

## 📦 Distribution

### 🎁 Pre-Built Packages
Get the Music Tools Suite with one-click installation:
- **Python Installer**: `music-tools-suite-python-v1.0.zip`
- **Docker Complete**: `music-tools-suite-docker-v1.0.zip`
- **Complete Source**: `music-tools-suite-source-v1.0.zip`

### 🛠️ For Distributors
```bash
# Create all distribution packages
./create_distribution.sh

# Generates ready-to-share packages in dist/ directory
```

📖 **Complete distribution guide**: See [`DISTRIBUTION.md`](DISTRIBUTION.md)

## 🆘 Support & Documentation

- **📖 Installation Help**: [`INSTALLATION.md`](INSTALLATION.md) - Step-by-step user guide
- **🔧 Distribution Info**: [`DISTRIBUTION.md`](DISTRIBUTION.md) - For sharing the application
- **🐛 Issues**: Create GitHub issues for bugs and feature requests
- **💬 Discussions**: GitHub Discussions for community support

## 🔮 Future Roadmap

- **🎨 Custom AI Models**: Support for different separation models
- **💾 Export Options**: Direct export to various audio formats
- **🎛️ Advanced Mixing**: EQ, effects, and processing tools
- **☁️ Cloud Processing**: Optional cloud-based separation for faster processing
- **📱 Mobile Optimization**: Enhanced mobile browser experience

---

**🎵 Ready to transform your music workflow?**

**Get started with the [Installation Guide](INSTALLATION.md) and start creating amazing mixes in minutes!** 