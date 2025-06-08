#!/usr/bin/env python3
"""
Music Tools Suite - One-Click Installer
Handles Python dependencies, FFmpeg installation, and setup.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    if shutil.which('ffmpeg'):
        print("✅ FFmpeg already installed")
        return True
    print("⚠️  FFmpeg not found")
    return False

def install_ffmpeg():
    """Install FFmpeg based on operating system"""
    system = platform.system().lower()
    
    print(f"🔧 Installing FFmpeg for {system}...")
    
    if system == "darwin":  # macOS
        if shutil.which('brew'):
            success, output = run_command(['brew', 'install', 'ffmpeg'])
            if success:
                print("✅ FFmpeg installed via Homebrew")
                return True
        else:
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
            
    elif system == "linux":
        # Try different package managers
        if shutil.which('apt'):
            success, output = run_command(['sudo', 'apt', 'update'])
            if success:
                success, output = run_command(['sudo', 'apt', 'install', '-y', 'ffmpeg'])
                if success:
                    print("✅ FFmpeg installed via apt")
                    return True
        elif shutil.which('yum'):
            success, output = run_command(['sudo', 'yum', 'install', '-y', 'ffmpeg'])
            if success:
                print("✅ FFmpeg installed via yum")
                return True
        elif shutil.which('pacman'):
            success, output = run_command(['sudo', 'pacman', '-S', 'ffmpeg'])
            if success:
                print("✅ FFmpeg installed via pacman")
                return True
        
    elif system == "windows":
        print("📋 For Windows, please manually install FFmpeg:")
        print("   1. Download from: https://ffmpeg.org/download.html")
        print("   2. Extract to C:\\ffmpeg")
        print("   3. Add C:\\ffmpeg\\bin to your PATH")
        print("   4. Restart your terminal and run this installer again")
        return False
    
    print(f"❌ Could not install FFmpeg automatically on {system}")
    return False

def create_venv():
    """Create virtual environment"""
    venv_path = Path("music_tools_env")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
        
    print("🔧 Creating virtual environment...")
    success, output = run_command([sys.executable, '-m', 'venv', str(venv_path)])
    
    if success:
        print("✅ Virtual environment created")
        return True
    else:
        print(f"❌ Failed to create virtual environment: {output}")
        return False

def get_venv_python():
    """Get path to virtual environment Python"""
    system = platform.system().lower()
    venv_path = Path("music_tools_env")
    
    if system == "windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def install_requirements():
    """Install Python requirements in virtual environment"""
    print("🔧 Installing Python dependencies...")
    
    venv_python = get_venv_python()
    
    # Upgrade pip first
    success, output = run_command([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'])
    if not success:
        print(f"⚠️  Warning: Could not upgrade pip: {output}")
    
    # Install requirements
    success, output = run_command([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    if success:
        print("✅ Python dependencies installed")
        return True
    else:
        print(f"❌ Failed to install dependencies: {output}")
        return False

def create_launcher_script():
    """Create launcher script"""
    system = platform.system().lower()
    venv_python = get_venv_python()
    
    if system == "windows":
        launcher_content = f"""@echo off
echo 🎵 Starting Music Tools Suite...
"{venv_python}" -m streamlit run app.py --browser.gatherUsageStats=false
pause
"""
        launcher_path = "launch_music_tools.bat"
    else:
        launcher_content = f"""#!/bin/bash
echo "🎵 Starting Music Tools Suite..."
"{venv_python}" -m streamlit run app.py --browser.gatherUsageStats=false
"""
        launcher_path = "launch_music_tools.sh"
    
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    if system != "windows":
        os.chmod(launcher_path, 0o755)
    
    print(f"✅ Launcher created: {launcher_path}")

def main():
    """Main installation process"""
    print("🎵 Music Tools Suite - One-Click Installer")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check/Install FFmpeg
    if not check_ffmpeg():
        if not install_ffmpeg():
            print("\n❌ FFmpeg installation failed.")
            print("Please install FFmpeg manually and run this installer again.")
            sys.exit(1)
    
    # Create virtual environment
    if not create_venv():
        sys.exit(1)
    
    # Install Python requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create launcher script
    create_launcher_script()
    
    print("\n" + "=" * 50)
    print("✅ Installation completed successfully!")
    print("\n🚀 To start the Music Tools Suite:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   Double-click: launch_music_tools.bat")
        print("   Or run: launch_music_tools.bat")
    else:
        print("   Run: ./launch_music_tools.sh")
        print("   Or: bash launch_music_tools.sh")
    
    print("\n📖 The app will open in your browser at: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - First run may take longer (AI model downloads)")
    print("   - Make sure you have a stable internet connection")
    print("   - For best performance, close other resource-intensive apps")

if __name__ == "__main__":
    main() 