import os
import shutil
import subprocess
import tempfile
import base64
from pathlib import Path
import streamlit as st

# ─── Page Configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="Music Tools Suite", 
    layout="wide", 
    page_icon="🎵"
)

# ─── Custom CSS Styling ─────────────────────────────────────────────
st.markdown("""
<style>
.main .block-container {
    max-width: 95%;
    padding: 1rem 2rem;
}

.section-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 0.5rem 1rem;
    margin: 02rem -2rem 1.5rem -2rem;
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.section-header h2 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: bold;
}

.section-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 1rem;
}

.workflow-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 5px solid #4CAF50;
}

.quick-action {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: white;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.stButton > button {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.status-success {
    background: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
}

.status-info {
    background: #d1ecf1;
    color: #0c5460;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #bee5eb;
}

#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Helper Functions ─────────────────────────────────────────────

def download_audio(youtube_url: str, output_dir: str) -> str:
    """Download YouTube audio and convert to MP3"""
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
        "-o", output_template, youtube_url
    ]
    subprocess.run(cmd, check=True)
    
    for fname in os.listdir(output_dir):
        if fname.endswith(".mp3"):
            return os.path.join(output_dir, fname)
    raise FileNotFoundError("MP3 not found after download")

def separate_stems(input_audio_path: str, output_dir: str) -> str:
    """Separate audio into stems using Demucs"""
    cmd = ["demucs", "--out", output_dir, input_audio_path]
    subprocess.run(cmd, check=True)
    
    # Find the stems folder in Demucs output structure
    for item in os.listdir(output_dir):
        full_path = os.path.join(output_dir, item)
        if os.path.isdir(full_path):
            for song_item in os.listdir(full_path):
                song_path = os.path.join(full_path, song_item)
                if os.path.isdir(song_path):
                    wav_files = [f for f in os.listdir(song_path) if f.endswith('.wav')]
                    if wav_files:
                        return song_path
    raise FileNotFoundError("Stems not found in expected structure")

def convert_stems_to_mp3(stems_folder: str, output_dir: str, base_name: str) -> list[str]:
    """Convert WAV stems to MP3"""
    mp3_files = []
    wav_files = [f for f in os.listdir(stems_folder) if f.endswith('.wav')]
    
    for file in wav_files:
        wav_path = os.path.join(stems_folder, file)
        stem_name = os.path.splitext(file)[0]
        mp3_filename = f"{base_name}_{stem_name}.mp3"
        mp3_path = os.path.join(output_dir, mp3_filename)
        
        cmd = ["ffmpeg", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "320k", "-y", mp3_path]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if os.path.exists(mp3_path):
                mp3_files.append(mp3_path)
        except subprocess.CalledProcessError:
            continue
    return mp3_files

def validate_and_create_path(path_str: str) -> tuple[bool, str]:
    """Validate and create directory if needed"""
    try:
        path = Path(path_str)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            return True, f"Created directory: {path}"
        elif not path.is_dir():
            return False, f"Path exists but is not a directory: {path}"
        else:
            return True, f"Using existing directory: {path}"
    except Exception as e:
        return False, f"Error with path: {e}"

def get_stem_icon(stem_name):
    """Get appropriate icon for stem type"""
    stem_name_lower = stem_name.lower()
    if 'vocal' in stem_name_lower:
        return "🎤"
    elif 'drum' in stem_name_lower:
        return "🥁"
    elif 'bass' in stem_name_lower:
        return "🎸"
    elif 'other' in stem_name_lower:
        return "🎵"
    else:
        return "🎶"

def create_audio_player_html(stems_data):
    """Create HTML audio player with synchronized playback"""
    audio_elements = []
    for i, (name, b64_data) in enumerate(stems_data.items()):
        audio_elements.append(f"""
            <audio id="audio_{i}" preload="auto">
                <source src="data:audio/mpeg;base64,{b64_data}" type="audio/mpeg">
            </audio>
        """)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
                         .player-container {{
                 font-family: Arial, sans-serif;
                 background: #1e1e1e;
                 padding: 20px;
                 border-radius: 10px;
                 color: white;
                 outline: none;
                 border: 2px solid transparent;
                 transition: border-color 0.3s ease;
             }}
             .player-container:focus {{
                 border-color: #4CAF50;
                 box-shadow: 0 0 15px rgba(76, 175, 80, 0.3);
             }}
             .keyboard-hint {{
                 position: absolute;
                 top: 10px;
                 right: 10px;
                 background: rgba(76, 175, 80, 0.8);
                 color: white;
                 padding: 5px 10px;
                 border-radius: 15px;
                 font-size: 12px;
                 opacity: 0;
                 transition: opacity 0.3s ease;
             }}
             .player-container:focus .keyboard-hint {{
                 opacity: 1;
             }}
            .master-controls {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: #2d2d2d;
                border-radius: 8px;
            }}
            .master-controls button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 0 5px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }}
            .master-controls button:hover {{ background: #45a049; }}
            .master-controls button.stop {{ background: #f44336; }}
            .master-controls button.stop:hover {{ background: #da190b; }}
            .stems-container {{
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-top: 20px;
            }}
            .stem-control {{
                background: #2d2d2d;
                padding: 20px;
                border-radius: 12px;
                border: 2px solid #444;
                display: flex;
                align-items: center;
                gap: 20px;
                transition: border-color 0.3s ease;
            }}
            .stem-control:hover {{ border-color: #4CAF50; }}
            .stem-icon {{
                font-size: 32px;
                min-width: 50px;
                text-align: center;
            }}
            .stem-info {{
                flex: 1;
                min-width: 0;
            }}
            .stem-name {{
                font-weight: bold;
                margin-bottom: 8px;
                color: #4CAF50;
                font-size: 18px;
            }}
            .stem-controls {{
                display: flex;
                flex-direction: column;
                gap: 12px;
                min-width: 250px;
            }}
            .control-row {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .control-label {{
                width: 70px;
                font-size: 13px;
                color: #ccc;
                font-weight: 500;
            }}
            input[type="range"] {{
                flex: 1;
                height: 6px;
                -webkit-appearance: none;
                background: #444;
                border-radius: 3px;
                outline: none;
            }}
            input[type="range"]::-webkit-slider-thumb {{
                -webkit-appearance: none;
                width: 18px;
                height: 18px;
                background: #4CAF50;
                border-radius: 50%;
                cursor: pointer;
            }}
            .volume-value {{
                min-width: 50px;
                text-align: right;
                font-size: 13px;
                color: #4CAF50;
                font-weight: 500;
            }}
            .control-buttons {{
                display: flex;
                gap: 10px;
                margin: 8px 0 0 0;
            }}
            .control-buttons button {{
                flex: 1;
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                font-weight: 500;
                transition: all 0.2s ease;
            }}
            .mute-btn {{ background: #ff9800; color: white; }}
            .mute-btn.active {{ background: #f44336; }}
            .solo-btn {{ background: #2196F3; color: white; }}
            .solo-btn.active {{ background: #4CAF50; }}
            .time-display {{
                text-align: center;
                margin: 15px 0;
                font-family: monospace;
                font-size: 18px;
                color: #4CAF50;
            }}
            .progress-bar {{
                width: 100%;
                height: 8px;
                background: #444;
                border-radius: 4px;
                overflow: hidden;
                margin: 10px 0;
                cursor: pointer;
            }}
                         .progress-fill {{
                 height: 100%;
                 background: #4CAF50;
                 width: 0%;
                 transition: width 0.1s;
             }}
             .stem-progress {{
                 margin-top: 8px;
             }}
             .progress-bar-small {{
                 width: 100%;
                 height: 4px;
                 background: #444;
                 border-radius: 2px;
                 overflow: hidden;
             }}
             .progress-fill-small {{
                 height: 100%;
                 background: #4CAF50;
                 width: 0%;
                 transition: width 0.1s;
             }}
             .fullscreen-btn {{
                 background: #9C27B0;
                 color: white;
                 margin-left: 10px;
             }}
             .fullscreen-btn:hover {{
                 background: #7B1FA2;
             }}
        </style>
    </head>
    <body>
                 <div class="player-container" tabindex="0">
             <div class="keyboard-hint">⌨️ Keyboard controls active</div>
             {''.join(audio_elements)}
            
            <div class="master-controls">
                <h3>Master Controls</h3>
                <button onclick="playAll()">▶️ Play</button>
                <button onclick="pauseAll()">⏸️ Pause</button>
                <button onclick="stopAll()" class="stop">⏹️ Stop</button>
                <button onclick="toggleFullscreen()" class="fullscreen-btn">🔳 Fullscreen</button>
                
                <div class="control-row" style="max-width: 350px; margin: 15px auto; gap: 15px;">
                    <span class="control-label" style="width: 80px;">Master:</span>
                    <input type="range" id="masterVolume" min="0" max="100" value="100" 
                           oninput="setMasterVolume(this.value)">
                    <span class="volume-value" id="masterVolumeValue">100%</span>
                </div>
                
                <div class="time-display">
                    <span id="currentTime">00:00</span> / <span id="totalTime">00:00</span>
                </div>
                
                <div class="progress-bar" onclick="seekTo(event)">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
            
            <div class="stems-container">
    """
    
    for i, name in enumerate(stems_data.keys()):
        icon = get_stem_icon(name)
        clean_name = name.replace('_', ' ').title()
        html_content += f"""
                <div class="stem-control">
                    <div class="stem-icon">{icon}</div>
                    <div class="stem-info">
                        <div class="stem-name">{clean_name}</div>
                    </div>
                    <div class="stem-controls">
                        <div class="control-row">
                            <span class="control-label">Volume:</span>
                            <input type="range" id="volume_{i}" min="0" max="100" value="100" 
                                   oninput="setStemVolume({i}, this.value)">
                            <span class="volume-value" id="volumeValue_{i}">100%</span>
                        </div>
                        <div class="control-buttons">
                            <button class="mute-btn" id="muteBtn_{i}" onclick="toggleMute({i})">
                                🔇 Mute
                            </button>
                            <button class="solo-btn" id="soloBtn_{i}" onclick="toggleSolo({i})">
                                🎯 Solo
                            </button>
                        </div>
                        <div class="stem-progress">
                            <div class="progress-bar-small">
                                <div class="progress-fill-small" id="stemProgress_{i}"></div>
                            </div>
                        </div>
                    </div>
                </div>
        """
    
        html_content += f"""
            </div>
        </div>
        
        <script>
            const audioElements = [{', '.join([f'document.getElementById("audio_{i}")' for i in range(len(stems_data))])}];
            let isPlaying = false;
            let soloedTrack = -1;
            const mutedTracks = new Set();
            
            audioElements.forEach((audio, i) => {{
                audio.addEventListener('loadedmetadata', () => {{
                    if (i === 0) updateTimeDisplay();
                }});
                audio.addEventListener('timeupdate', () => {{
                    updateStemProgress(i);
                    if (i === 0) {{
                        updateTimeDisplay();
                        updateProgressBar();
                    }}
                }});
            }});
            
            function playAll() {{
                const currentTime = audioElements[0].currentTime;
                audioElements.forEach(audio => {{
                    audio.currentTime = currentTime;
                    audio.play();
                }});
                isPlaying = true;
            }}
            
            function pauseAll() {{
                audioElements.forEach(audio => audio.pause());
                isPlaying = false;
            }}
            
            function stopAll() {{
                audioElements.forEach(audio => {{
                    audio.pause();
                    audio.currentTime = 0;
                }});
                isPlaying = false;
                updateTimeDisplay();
                updateProgressBar();
            }}
            
            function setMasterVolume(value) {{
                const volume = value / 100;
                audioElements.forEach((audio, i) => {{
                    if (!mutedTracks.has(i) && (soloedTrack === -1 || soloedTrack === i)) {{
                        const stemVolume = document.getElementById(`volume_${{i}}`).value / 100;
                        audio.volume = volume * stemVolume;
                    }}
                }});
                document.getElementById('masterVolumeValue').textContent = value + '%';
            }}
            
            function setStemVolume(index, value) {{
                const volume = value / 100;
                const masterVolume = document.getElementById('masterVolume').value / 100;
                if (!mutedTracks.has(index) && (soloedTrack === -1 || soloedTrack === index)) {{
                    audioElements[index].volume = volume * masterVolume;
                }}
                document.getElementById(`volumeValue_${{index}}`).textContent = value + '%';
            }}
            
            function toggleMute(index) {{
                const btn = document.getElementById(`muteBtn_${{index}}`);
                if (mutedTracks.has(index)) {{
                    mutedTracks.delete(index);
                    btn.classList.remove('active');
                    btn.textContent = '🔇 Mute';
                    if (soloedTrack === -1 || soloedTrack === index) {{
                        const stemVolume = document.getElementById(`volume_${{index}}`).value / 100;
                        const masterVolume = document.getElementById('masterVolume').value / 100;
                        audioElements[index].volume = stemVolume * masterVolume;
                    }}
                }} else {{
                    mutedTracks.add(index);
                    btn.classList.add('active');
                    btn.textContent = '🔊 Unmute';
                    audioElements[index].volume = 0;
                }}
            }}
            
            function toggleSolo(index) {{
                const btn = document.getElementById(`soloBtn_${{index}}`);
                if (soloedTrack === index) {{
                    soloedTrack = -1;
                    btn.classList.remove('active');
                    btn.textContent = '🎯 Solo';
                    audioElements.forEach((audio, i) => {{
                        if (!mutedTracks.has(i)) {{
                            const stemVolume = document.getElementById(`volume_${{i}}`).value / 100;
                            const masterVolume = document.getElementById('masterVolume').value / 100;
                            audio.volume = stemVolume * masterVolume;
                        }}
                    }});
                }} else {{
                    if (soloedTrack !== -1) {{
                        const prevBtn = document.getElementById(`soloBtn_${{soloedTrack}}`);
                        prevBtn.classList.remove('active');
                        prevBtn.textContent = '🎯 Solo';
                    }}
                    soloedTrack = index;
                    btn.classList.add('active');
                    btn.textContent = '🔇 Unsolo';
                    audioElements.forEach((audio, i) => {{
                        if (i === index && !mutedTracks.has(i)) {{
                            const stemVolume = document.getElementById(`volume_${{i}}`).value / 100;
                            const masterVolume = document.getElementById('masterVolume').value / 100;
                            audio.volume = stemVolume * masterVolume;
                        }} else {{
                            audio.volume = 0;
                        }}
                    }});
                }}
            }}
            
            function updateTimeDisplay() {{
                if (audioElements[0]) {{
                    const current = audioElements[0].currentTime;
                    const total = audioElements[0].duration || 0;
                    document.getElementById('currentTime').textContent = formatTime(current);
                    document.getElementById('totalTime').textContent = formatTime(total);
                }}
            }}
            
            function updateProgressBar() {{
                if (audioElements[0]) {{
                    const current = audioElements[0].currentTime;
                    const total = audioElements[0].duration || 0;
                    const progress = total > 0 ? (current / total) * 100 : 0;
                    document.getElementById('progressFill').style.width = progress + '%';
                }}
            }}
            
            function updateStemProgress(index) {{
                if (audioElements[index]) {{
                    const current = audioElements[index].currentTime;
                    const total = audioElements[index].duration || 0;
                    const progress = total > 0 ? (current / total) * 100 : 0;
                    const progressElement = document.getElementById(`stemProgress_${{index}}`);
                    if (progressElement) {{
                        progressElement.style.width = progress + '%';
                    }}
                }}
            }}
            
            function seekTo(event) {{
                if (audioElements[0] && audioElements[0].duration) {{
                    const progressBar = event.currentTarget;
                    const rect = progressBar.getBoundingClientRect();
                    const clickX = event.clientX - rect.left;
                    const percentage = clickX / rect.width;
                    const newTime = percentage * audioElements[0].duration;
                    audioElements.forEach(audio => {{
                        audio.currentTime = newTime;
                    }});
                }}
            }}
            
            function formatTime(seconds) {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}
            
            function toggleFullscreen() {{
                const container = document.querySelector('.player-container');
                if (!document.fullscreenElement) {{
                    container.requestFullscreen().catch(err => {{
                        console.log('Error attempting to enable fullscreen:', err);
                    }});
                }} else {{
                    document.exitFullscreen();
                }}
            }}
            
            // Handle fullscreen changes
            document.addEventListener('fullscreenchange', () => {{
                const container = document.querySelector('.player-container');
                if (document.fullscreenElement) {{
                    container.style.padding = '40px';
                    container.style.height = '100vh';
                    container.style.overflowY = 'auto';
                }} else {{
                    container.style.padding = '20px';
                    container.style.height = 'auto';
                    container.style.overflowY = 'visible';
                }}
            }});
            
            // Keyboard Controls
            document.addEventListener('keydown', (event) => {{
                const key = event.key.toLowerCase();
                const ctrlKey = event.ctrlKey || event.metaKey;
                
                // Don't interfere if user is typing in an input field
                if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {{
                    return;
                }}
                
                switch(key) {{
                    case ' ':
                    case 'spacebar':
                        event.preventDefault();
                        if (isPlaying) {{
                            pauseAll();
                        }} else {{
                            playAll();
                        }}
                        break;
                        
                    case 's':
                    case 'escape':
                        event.preventDefault();
                        stopAll();
                        break;
                        
                    case 'f':
                        if (!ctrlKey) {{
                            event.preventDefault();
                            toggleFullscreen();
                        }}
                        break;
                        
                    case 'arrowleft':
                        event.preventDefault();
                        seekRelative(-10);
                        break;
                        
                    case 'arrowright':
                        event.preventDefault();
                        seekRelative(10);
                        break;
                        
                    case 'arrowup':
                        event.preventDefault();
                        adjustMasterVolume(5);
                        break;
                        
                    case 'arrowdown':
                        event.preventDefault();
                        adjustMasterVolume(-5);
                        break;
                        
                    case 'm':
                        event.preventDefault();
                        toggleMasterMute();
                        break;
                        
                    case '1':
                    case '2':
                    case '3':
                    case '4':
                    case '5':
                    case '6':
                    case '7':
                    case '8':
                    case '9':
                        event.preventDefault();
                        const stemIndex = parseInt(key) - 1;
                        if (stemIndex < audioElements.length) {{
                            toggleSolo(stemIndex);
                        }}
                        break;
                        
                    case '!':
                    case '@':
                    case '#':
                    case '$':
                    case '%':
                    case '^':
                    case '&':
                    case '*':
                    case '(':
                        event.preventDefault();
                        const shiftKeys = {{'!': 0, '@': 1, '#': 2, '$': 3, '%': 4, '^': 5, '&': 6, '*': 7, '(': 8}};
                        const muteIndex = shiftKeys[key];
                        if (muteIndex < audioElements.length) {{
                            toggleMute(muteIndex);
                        }}
                        break;
                }}
            }});
            
            // Helper functions for keyboard controls
            function seekRelative(seconds) {{
                if (audioElements[0] && audioElements[0].duration) {{
                    const newTime = Math.max(0, Math.min(audioElements[0].duration, audioElements[0].currentTime + seconds));
                    audioElements.forEach(audio => {{
                        audio.currentTime = newTime;
                    }});
                }}
            }}
            
            function adjustMasterVolume(delta) {{
                const masterVolumeSlider = document.getElementById('masterVolume');
                const currentValue = parseInt(masterVolumeSlider.value);
                const newValue = Math.max(0, Math.min(100, currentValue + delta));
                masterVolumeSlider.value = newValue;
                setMasterVolume(newValue);
            }}
            
            let masterMuted = false;
            let previousMasterVolume = 100;
            
            function toggleMasterMute() {{
                const masterVolumeSlider = document.getElementById('masterVolume');
                
                if (masterMuted) {{
                    masterVolumeSlider.value = previousMasterVolume;
                    setMasterVolume(previousMasterVolume);
                    masterMuted = false;
                }} else {{
                    previousMasterVolume = masterVolumeSlider.value;
                    masterVolumeSlider.value = 0;
                    setMasterVolume(0);
                    masterMuted = true;
                }}
            }}
            
            // Initialize player focus
            const playerContainer = document.querySelector('.player-container');
            
            setTimeout(() => {{
                playerContainer.focus();
            }}, 100);
            
            playerContainer.addEventListener('click', () => {{
                playerContainer.focus();
            }});
            
            setTimeout(() => {{
                playerContainer.style.borderColor = '#4CAF50';
                setTimeout(() => {{
                    if (document.activeElement !== playerContainer) {{
                        playerContainer.style.borderColor = 'transparent';
                    }}
                }}, 3000);
            }}, 500);
            
            updateTimeDisplay();
        </script>
    </body>
    </html>
    """
    return html_content

# Initialize session state
if 'downloaded_mp3' not in st.session_state:
    st.session_state.downloaded_mp3 = None
if 'separated_stems' not in st.session_state:
    st.session_state.separated_stems = None
if 'default_folder' not in st.session_state:
    st.session_state.default_folder = str(Path.home() / "Downloads")
if 'fullscreen_player' not in st.session_state:
    st.session_state.fullscreen_player = False

# ─── Main Application ─────────────────────────────────────────────

st.title("🎵 Music Tools Suite")
st.markdown("**YouTube → MP3 → Stems → Player**")

# ═══════════════════════════════════════════════════════════════════
# ─── 1. YOUTUBE TO MP3 ─────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <h2>🎬 1. YouTube to MP3</h2>
    <p>Download and convert YouTube videos to high-quality MP3 files</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

with col2:
    mp3_save_path = st.text_input("Save folder", value=st.session_state.default_folder)

if st.button("🚀 Download MP3", type="primary"):
    if not youtube_url.strip():
        st.error("Please enter a valid YouTube URL.")
    else:
        # Validate save path
        path_valid, path_msg = validate_and_create_path(mp3_save_path)
        if not path_valid:
            st.error(path_msg)
        else:
            st.info(path_msg)
            
            # Download process
            with tempfile.TemporaryDirectory() as tmpdir:
                try:
                    with st.spinner("Downloading and converting to MP3..."):
                        mp3_path = download_audio(youtube_url, tmpdir)
                    
                    # Save to local directory
                    mp3_filename = os.path.basename(mp3_path)
                    local_mp3_path = os.path.join(mp3_save_path, mp3_filename)
                    shutil.copy2(mp3_path, local_mp3_path)
                    
                    # Update session state
                    st.session_state.downloaded_mp3 = local_mp3_path
                    st.session_state.default_folder = mp3_save_path
                    
                    st.success(f"✅ MP3 saved: `{local_mp3_path}`")
                    
                    # Provide download button
                    with open(mp3_path, "rb") as f:
                        st.download_button(
                            "📁 Download MP3 File",
                            data=f.read(),
                            file_name=mp3_filename,
                            mime="audio/mpeg"
                        )
                    
                except subprocess.CalledProcessError:
                    st.error("Error downloading from YouTube. Check the URL and try again.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

# Show quick action if MP3 was just downloaded
if st.session_state.downloaded_mp3:
    st.markdown("""
    <div class="quick-action">
        <h4>🎯 Quick Action: Separate to Stems</h4>
        <p>Your MP3 is ready! Want to separate it into individual instrument tracks?</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# ─── 2. SEPARATE MP3 TO STEMS ──────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <h2>🎛️ 2. Separate MP3 to Stems</h2>
    <p>Use AI to separate audio into individual tracks: vocals, drums, bass, other</p>
</div>
""", unsafe_allow_html=True)

# Source selection
source_option = st.radio(
    "Choose MP3 source:",
    options=["Use downloaded MP3" if st.session_state.downloaded_mp3 else "No MP3 downloaded", "Upload existing MP3 file"],
    index=0 if st.session_state.downloaded_mp3 else 1
)

mp3_to_separate = None

if source_option.startswith("Use downloaded MP3") and st.session_state.downloaded_mp3:
    mp3_to_separate = st.session_state.downloaded_mp3
    st.success(f"Using: `{os.path.basename(mp3_to_separate)}`")
    
elif source_option == "Upload existing MP3 file":
    uploaded_mp3 = st.file_uploader("Choose MP3 file", type=['mp3'], key="mp3_upload")
    if uploaded_mp3:
        # Save uploaded file temporarily
        temp_mp3_path = os.path.join(tempfile.gettempdir(), uploaded_mp3.name)
        with open(temp_mp3_path, "wb") as f:
            f.write(uploaded_mp3.read())
        mp3_to_separate = temp_mp3_path
        st.success(f"Loaded: `{uploaded_mp3.name}`")

# Stems save path
stems_save_path = st.text_input("Save stems folder", value=st.session_state.default_folder, key="stems_path")

if mp3_to_separate and st.button("🚀 Separate to Stems", type="primary"):
    # Validate stems save path
    path_valid, path_msg = validate_and_create_path(stems_save_path)
    if not path_valid:
        st.error(path_msg)
    else:
        st.info(path_msg)
        
        # Separation process
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                with st.spinner("Separating stems with AI (this may take several minutes)..."):
                    stems_folder = separate_stems(mp3_to_separate, tmpdir)
                
                st.success("✅ Stem separation complete!")
                
                # Convert stems to MP3
                with st.spinner("Converting stems to MP3..."):
                    base_name = os.path.splitext(os.path.basename(mp3_to_separate))[0]
                    stem_mp3_files = convert_stems_to_mp3(stems_folder, stems_save_path, base_name)
                
                if stem_mp3_files:
                    st.session_state.separated_stems = stem_mp3_files
                    st.session_state.default_folder = stems_save_path
                    st.success(f"✅ {len(stem_mp3_files)} stem files saved to: `{stems_save_path}`")
                    
                    # Show individual stem files
                    for stem_file in stem_mp3_files:
                        st.success(f"   • {os.path.basename(stem_file)}")
                    
                    # Provide download buttons
                    st.subheader("Download Individual Stems")
                    cols = st.columns(min(len(stem_mp3_files), 4))
                    
                    for i, stem_file in enumerate(stem_mp3_files):
                        with open(stem_file, "rb") as f:
                            stem_bytes = f.read()
                        
                        col_idx = i % len(cols)
                        with cols[col_idx]:
                            st.download_button(
                                f"📁 {os.path.basename(stem_file)}",
                                data=stem_bytes,
                                file_name=os.path.basename(stem_file),
                                mime="audio/mpeg",
                                key=f"stem_download_{i}"
                            )
                else:
                    st.error("❌ No stem files were created!")
                    
            except subprocess.CalledProcessError:
                st.error("Error running Demucs. Make sure Demucs is installed.")
            except Exception as e:
                st.error(f"Unexpected error during separation: {e}")

# Show quick action if stems were just separated
if st.session_state.separated_stems:
    st.markdown("""
    <div class="quick-action">
        <h4>🎯 Quick Action: Play & Mix Stems</h4>
        <p>Your stems are ready! Want to load them into the player for mixing?</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# ─── 3. PLAY STEMS ─────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <h2>🎚️ 3. Play & Mix Stems</h2>
    <p>Professional mixing interface with synchronized playback and individual controls</p>
</div>
""", unsafe_allow_html=True)

# Source selection for stems
stem_source_option = st.radio(
    "Choose stem source:",
    options=[
        "Use separated stems" if st.session_state.separated_stems else "No stems separated",
        "Upload stem files"
    ],
    index=0 if st.session_state.separated_stems else 1,
    key="stem_source"
)

stems_to_play = None

if stem_source_option.startswith("Use separated stems") and st.session_state.separated_stems:
    stems_to_play = st.session_state.separated_stems
    st.success(f"Using {len(stems_to_play)} separated stem files")
    
    # Show loaded stems
    with st.expander("📋 Loaded Stems", expanded=True):
        for stem_file in stems_to_play:
            file_size = os.path.getsize(stem_file) / 1024  # KB
            st.write(f"🎛️ {os.path.basename(stem_file)} ({file_size:.1f} KB)")
            
elif stem_source_option == "Upload stem files":
    uploaded_stems = st.file_uploader(
        "Choose stem files",
        type=['mp3', 'wav'],
        accept_multiple_files=True,
        help="Upload separated stem files (vocals, drums, bass, other, etc.)",
        key="stems_upload"
    )
    
    if uploaded_stems and len(uploaded_stems) >= 2:
        stems_to_play = uploaded_stems
        st.success(f"Loaded {len(uploaded_stems)} stem files")
        
        # Show uploaded files
        with st.expander("📋 Uploaded Files", expanded=True):
            for file in uploaded_stems:
                st.write(f"🎵 {file.name} ({file.size / 1024:.1f} KB)")
    elif uploaded_stems and len(uploaded_stems) < 2:
        st.warning("Please upload at least 2 stem files for mixing.")

# Create and display the player
if stems_to_play:
    st.subheader("🎛️ Professional Stem Player")
    
    # Prepare stems data
    stems_data = {}
    
    with st.spinner("Preparing audio player..."):
        if isinstance(stems_to_play[0], str):  # File paths (from separation)
            for file_path in stems_to_play:
                stem_name = Path(file_path).stem
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    audio_base64 = base64.b64encode(file_bytes).decode()
                    stems_data[stem_name] = audio_base64
        else:  # Uploaded files
            for uploaded_file in stems_to_play:
                stem_name = Path(uploaded_file.name).stem
                file_bytes = uploaded_file.read()
                audio_base64 = base64.b64encode(file_bytes).decode()
                stems_data[stem_name] = audio_base64
    
    # Display the player
    if stems_data:
        # Player view options
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("📱 Compact View", use_container_width=True):
                st.session_state.fullscreen_player = False
                st.rerun()
        with col2:
            if st.button("🖥️ Expanded View", use_container_width=True):
                st.session_state.fullscreen_player = True
                st.rerun()
        with col3:
            st.write(f"**Current:** {'Expanded' if st.session_state.fullscreen_player else 'Compact'} View")
        
        # Create and display player
        player_html = create_audio_player_html(stems_data)
        player_height = 900 if st.session_state.fullscreen_player else 600
        st.components.v1.html(player_html, height=player_height, scrolling=True)
        
        st.markdown("""
        ---
        ### 🎯 Player Controls:
        - **▶️ Play/⏸️ Pause/⏹️ Stop**: Control all stems together
        - **🔳 Fullscreen**: Browser fullscreen mode (press Esc to exit)
        - **Master Volume**: Adjust overall volume of all stems
        - **Individual Volume**: Fine-tune each stem independently
        - **🔇 Mute**: Silence specific stems (red when active)
        - **🎯 Solo**: Isolate individual stems (green when active)
        - **Progress Bars**: Master progress + individual stem progress indicators
        - **Seek Control**: Click master progress bar to seek to any position
        - **View Options**: Switch between Compact and Expanded player views
        """)
        
        # Keyboard shortcuts in an expandable section
        with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🎵 Playback Controls:**
                - `Spacebar` - Play/Pause
                - `S` or `Esc` - Stop
                - `F` - Toggle Fullscreen
                - `M` - Master Mute/Unmute
                
                **🎚️ Volume & Seeking:**
                - `↑/↓` - Master Volume ±5%
                - `←/→` - Seek ±10 seconds
                """)
            
            with col2:
                st.markdown("""
                **🎛️ Individual Stem Controls:**
                - `1-9` - Solo/Unsolo stem (by position)
                - `Shift+1-9` - Mute/Unmute stem
                
                **💡 Tips:**
                - Click player area first to activate shortcuts
                - Shortcuts won't work while typing in input fields
                - Press `Esc` to exit fullscreen mode
                """)

else:
    st.info("👆 Upload stem files or separate MP3 above to start mixing!")
    
    st.markdown("""
    ### 💡 Tips for Best Results:
    - **Stem Separation**: Use the separator above to create individual tracks
    - **File Formats**: MP3 and WAV files are supported
    - **Synchronized Playback**: All stems play perfectly in sync
    - **Professional Controls**: Individual mute, solo, and volume controls
    - **File Naming**: Use descriptive names like `song_vocals.mp3`, `song_drums.mp3`
    """)


