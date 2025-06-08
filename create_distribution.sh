#!/bin/bash

# Music Tools Suite - Distribution Package Creator
echo "🎵 Music Tools Suite - Creating Distribution Packages"
echo "====================================================="

VERSION="1.0"
PROJECT_NAME="music-tools-suite"

# Create base directory for all packages
mkdir -p dist

echo "📦 Creating distribution packages..."

# ─── Package 1: Python Installer ───────────────────────────────
echo "🐍 Creating Python installer package..."
PYTHON_DIST="dist/${PROJECT_NAME}-python-v${VERSION}"
mkdir -p "$PYTHON_DIST"

# Copy essential files for Python distribution
cp app.py "$PYTHON_DIST/"
cp requirements.txt "$PYTHON_DIST/"
cp install.py "$PYTHON_DIST/"
cp README.md "$PYTHON_DIST/"
cp INSTALLATION.md "$PYTHON_DIST/"

# Create package archive
cd dist
zip -r "${PROJECT_NAME}-python-v${VERSION}.zip" "${PROJECT_NAME}-python-v${VERSION}/"
tar -czf "${PROJECT_NAME}-python-v${VERSION}.tar.gz" "${PROJECT_NAME}-python-v${VERSION}/"
cd ..

echo "✅ Python package created: ${PROJECT_NAME}-python-v${VERSION}.zip"

# ─── Package 2: Docker Complete ────────────────────────────────
echo "🐳 Creating Docker complete package..."
DOCKER_DIST="dist/${PROJECT_NAME}-docker-v${VERSION}"
mkdir -p "$DOCKER_DIST"

# Copy all Docker-related files
cp app.py "$DOCKER_DIST/"
cp requirements.txt "$DOCKER_DIST/"
cp Dockerfile "$DOCKER_DIST/"
cp docker-compose.yml "$DOCKER_DIST/"
cp start_docker.sh "$DOCKER_DIST/"
cp start_docker.bat "$DOCKER_DIST/"
cp README.md "$DOCKER_DIST/"
cp INSTALLATION.md "$DOCKER_DIST/"

# Make scripts executable
chmod +x "$DOCKER_DIST/start_docker.sh"

# Create package archive
cd dist
zip -r "${PROJECT_NAME}-docker-v${VERSION}.zip" "${PROJECT_NAME}-docker-v${VERSION}/"
tar -czf "${PROJECT_NAME}-docker-v${VERSION}.tar.gz" "${PROJECT_NAME}-docker-v${VERSION}/"
cd ..

echo "✅ Docker package created: ${PROJECT_NAME}-docker-v${VERSION}.zip"

# ─── Package 3: Complete Source ────────────────────────────────
echo "📁 Creating complete source package..."
SOURCE_DIST="dist/${PROJECT_NAME}-source-v${VERSION}"
mkdir -p "$SOURCE_DIST"

# Copy all source files (except .git and dist)
cp app.py "$SOURCE_DIST/"
cp requirements.txt "$SOURCE_DIST/"
cp install.py "$SOURCE_DIST/"
cp Dockerfile "$SOURCE_DIST/"
cp docker-compose.yml "$SOURCE_DIST/"
cp start_docker.sh "$SOURCE_DIST/"
cp start_docker.bat "$SOURCE_DIST/"
cp README.md "$SOURCE_DIST/"
cp INSTALLATION.md "$SOURCE_DIST/"
cp DISTRIBUTION.md "$SOURCE_DIST/"
cp .gitignore "$SOURCE_DIST/"

# Make scripts executable
chmod +x "$SOURCE_DIST/start_docker.sh"

# Create package archive
cd dist
zip -r "${PROJECT_NAME}-source-v${VERSION}.zip" "${PROJECT_NAME}-source-v${VERSION}/"
tar -czf "${PROJECT_NAME}-source-v${VERSION}.tar.gz" "${PROJECT_NAME}-source-v${VERSION}/"
cd ..

echo "✅ Source package created: ${PROJECT_NAME}-source-v${VERSION}.zip"

# ─── Create Release Notes ───────────────────────────────────────
echo "📝 Creating release documentation..."

cat > "dist/RELEASE_NOTES_v${VERSION}.md" << EOF
# Music Tools Suite v${VERSION} - Release Notes

## 🎵 What's Included

### Core Features:
- **YouTube to MP3**: High-quality audio downloads (320kbps)
- **AI Stem Separation**: Vocals, drums, bass, other tracks using Meta's Demucs
- **Professional Mixer**: Synchronized playback with individual controls
- **Keyboard Shortcuts**: Professional workflow controls
- **Smart Folder Management**: Persistent folder settings across operations

### Technical Features:
- Cross-platform support (Windows, Mac, Linux)
- Web-based interface (runs in browser)
- Professional audio processing pipeline
- Automatic dependency management
- Docker containerization support

## 📦 Distribution Packages

### 1. Python Installer (Recommended for most users)
**File:** \`${PROJECT_NAME}-python-v${VERSION}.zip\`
- **Size:** ~50MB (plus dependencies)
- **Requirements:** Python 3.8+
- **Installation:** Run \`python install.py\`
- **Best for:** General users, developers

### 2. Docker Complete (Most reliable)
**File:** \`${PROJECT_NAME}-docker-v${VERSION}.zip\`
- **Size:** ~2GB (includes all dependencies)
- **Requirements:** Docker Desktop
- **Installation:** Run platform-specific launcher script
- **Best for:** Tech users, server deployment

### 3. Complete Source
**File:** \`${PROJECT_NAME}-source-v${VERSION}.zip\`
- **Size:** ~100MB
- **Requirements:** Development environment
- **Installation:** Manual setup
- **Best for:** Developers, customization

## 🚀 Quick Start

### Python Installation:
1. Download \`${PROJECT_NAME}-python-v${VERSION}.zip\`
2. Extract and run: \`python install.py\`
3. Launch with generated script
4. Open browser to http://localhost:8501

### Docker Installation:
1. Download \`${PROJECT_NAME}-docker-v${VERSION}.zip\`
2. Extract and run platform launcher script
3. Open browser to http://localhost:8501

## 🔧 System Requirements

**Minimum:**
- RAM: 4GB (8GB recommended)
- Storage: 2GB free space
- Internet connection (for downloads and AI models)

**Supported Operating Systems:**
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, other distros)

## 📋 Installation Support

### Documentation:
- \`INSTALLATION.md\` - User installation guide
- \`README.md\` - Detailed feature documentation
- \`DISTRIBUTION.md\` - Advanced distribution guide

### Troubleshooting:
- Python method handles FFmpeg installation automatically
- Docker method includes all dependencies
- First run downloads AI models (~2GB) - be patient!

## 🆕 What's New in v${VERSION}

- ✅ Initial release
- ✅ Complete music processing pipeline
- ✅ Professional mixing interface
- ✅ Cross-platform installation support
- ✅ Docker containerization
- ✅ Comprehensive documentation

## 📞 Support

- **Issues:** Create GitHub issue
- **Documentation:** Check included README.md
- **Email:** [your-email@domain.com]

---

**🎵 Happy music mixing!**
EOF

echo "✅ Release notes created: RELEASE_NOTES_v${VERSION}.md"

# ─── Create Distribution Summary ────────────────────────────────
echo ""
echo "🎉 Distribution packages created successfully!"
echo ""
echo "📦 Available packages:"
echo "   📁 dist/${PROJECT_NAME}-python-v${VERSION}.zip    (Python installer)"
echo "   📁 dist/${PROJECT_NAME}-docker-v${VERSION}.zip    (Docker complete)"
echo "   📁 dist/${PROJECT_NAME}-source-v${VERSION}.zip    (Complete source)"
echo ""
echo "📝 Documentation:"
echo "   📄 dist/RELEASE_NOTES_v${VERSION}.md"
echo ""
echo "🔢 Package sizes:"
ls -lh dist/*.zip | awk '{print "   " $9 ": " $5}'
echo ""
echo "🚀 Next steps:"
echo "   1. Test packages on clean systems"
echo "   2. Upload to release platform (GitHub, etc.)"
echo "   3. Share installation links with users"
echo ""
echo "💡 For GitHub releases:"
echo "   git tag v${VERSION}"
echo "   git push origin v${VERSION}"
echo "   Upload dist/*.zip files to GitHub release" 