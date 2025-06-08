@echo off
echo 🎵 Music Tools Suite - Docker Launcher
echo ======================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first:
    echo    https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is ready

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🔧 Building and starting with docker-compose...
    docker-compose up --build -d
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Music Tools Suite is running!
        echo 🌐 Open your browser and go to: http://localhost:8501
        echo.
        echo 📋 Useful commands:
        echo    Stop:     docker-compose down
        echo    Restart:  docker-compose restart
        echo    Logs:     docker-compose logs -f
        echo    Update:   docker-compose pull ^&^& docker-compose up --build -d
    ) else (
        echo ❌ Failed to start with docker-compose
        pause
        exit /b 1
    )
) else (
    echo 🔧 Building and starting with Docker...
    
    REM Build the image
    docker build -t music-tools-suite .
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to build Docker image
        pause
        exit /b 1
    )
    
    REM Create downloads directory if it doesn't exist
    if not exist downloads mkdir downloads
    
    REM Stop and remove existing container if it exists
    docker stop music-tools-suite >nul 2>&1
    docker rm music-tools-suite >nul 2>&1
    
    REM Run the container
    docker run -d --name music-tools-suite -p 8501:8501 -v "%cd%\downloads:/app/downloads" --restart unless-stopped music-tools-suite
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Music Tools Suite is running!
        echo 🌐 Open your browser and go to: http://localhost:8501
        echo.
        echo 📋 Useful commands:
        echo    Stop:     docker stop music-tools-suite
        echo    Start:    docker start music-tools-suite
        echo    Restart:  docker restart music-tools-suite
        echo    Logs:     docker logs -f music-tools-suite
        echo    Remove:   docker stop music-tools-suite ^&^& docker rm music-tools-suite
    ) else (
        echo ❌ Failed to start Docker container
        pause
        exit /b 1
    )
)

echo.
echo 💡 Tips:
echo    - First startup may take a few minutes (downloading AI models)
echo    - Downloaded files will be saved to: %cd%\downloads
echo    - The app will automatically restart if it crashes

pause 