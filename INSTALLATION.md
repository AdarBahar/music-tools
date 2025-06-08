# Music Tools Suite - Installation Guide

🎵 **One-click installation for the complete music processing toolkit**

## Quick Start (Choose Your Method)

### 🐍 Method 1: Python Installation (Recommended)
**Best for most users - works on Windows, Mac, and Linux**

1. **Install Python 3.8+** (if not already installed)
   - Download from: https://python.org/downloads/
   - ✅ Make sure to check "Add Python to PATH" during installation

2. **Download & Install Music Tools Suite**
   ```bash
   # Download the package and extract it
   # Then run the installer:
   python install.py
   ```

3. **Launch the Application**
   - **Windows:** Double-click `launch_music_tools.bat`
   - **Mac/Linux:** Double-click `launch_music_tools.sh` or run `./launch_music_tools.sh`

4. **Open in Browser**
   - The app will automatically open at: http://localhost:8501

---

### 🐳 Method 2: Docker Installation (Most Reliable)
**Best for tech users - guaranteed to work everywhere**

1. **Install Docker Desktop**
   - Download from: https://docs.docker.com/get-docker/
   - Start Docker Desktop after installation

2. **Download & Run Music Tools Suite**
   ```bash
   # Download the Docker package and extract it
   # Then run the launcher:
   
   # Windows: Double-click start_docker.bat
   # Mac/Linux: Double-click start_docker.sh
   ```

3. **Open in Browser**
   - Go to: http://localhost:8501

---

## ✅ System Requirements

### Minimum Requirements:
- **RAM:** 4GB (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Required for downloads and AI models
- **Python:** 3.8+ (for Python installation method)
- **Docker:** Latest version (for Docker method)

### Operating Systems:
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, other distros)

---

## 🚀 First Time Setup

1. **Launch the application** using your chosen method
2. **Wait for initial setup** (first run downloads AI models - may take 5-10 minutes)
3. **Configure default folder** (optional - defaults to Downloads)
4. **Start using the tools!**

---

## 🎯 Quick Feature Overview

**🎬 YouTube to MP3**
- Paste any YouTube URL
- Download high-quality MP3 (320kbps)
- Saves to your chosen folder

**🎛️ AI Stem Separation**
- Separate any song into: vocals, drums, bass, other
- Uses cutting-edge AI (Meta's Demucs)
- Professional quality results

**🎚️ Professional Mixer**
- Play all stems in perfect sync
- Individual volume, mute, solo controls
- Keyboard shortcuts for pro workflow
- Export your custom mixes

---

## ❓ Troubleshooting

### Common Issues:

**"Python not found"**
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation
- Restart your terminal/command prompt

**"Docker not running"**
- Make sure Docker Desktop is installed and started
- Look for Docker icon in system tray (should show "running")

**"App won't load in browser"**
- Wait 2-3 minutes for full startup
- Try refreshing the page
- Check that no other app is using port 8501

**"FFmpeg not found" (Python method)**
- The installer will try to install FFmpeg automatically
- Manual installation: https://ffmpeg.org/download.html

**"AI models downloading slowly"**
- First run needs to download ~2GB of AI models
- Ensure stable internet connection
- Be patient - this only happens once

### Still Having Issues?
- Check the full documentation in README.md
- Create an issue on GitHub
- Email support: [your-email]

---

## 🔧 Advanced Configuration

### Changing Default Settings:
- Default download folder: Edit the "Save folder" field
- Memory usage: Close other applications for better performance
- Port conflicts: Edit the launch scripts to use different ports

### Performance Tips:
- Close resource-intensive applications
- Use SSD storage for better performance
- Ensure 4GB+ RAM available
- Stable internet connection for downloads

---

## 🆕 Updates

### Updating the Application:
**Python Method:**
```bash
# Re-run the installer
python install.py
```

**Docker Method:**
```bash
# Windows: Run start_docker.bat again
# Mac/Linux: Run ./start_docker.sh again
```

---

## 📞 Support

- **Documentation:** README.md (detailed guide)
- **Issues:** [GitHub Issues Link]
- **Email:** [your-email@domain.com]
- **Video Tutorial:** [YouTube Link]

---

**🎵 Enjoy creating amazing music mixes with the Music Tools Suite!** 