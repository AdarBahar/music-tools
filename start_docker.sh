#!/bin/bash

# Music Tools Suite - Docker Launcher
echo "🎵 Music Tools Suite - Docker Launcher"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is ready"

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "🔧 Building and starting with docker-compose..."
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Music Tools Suite is running!"
        echo "🌐 Open your browser and go to: http://localhost:8501"
        echo ""
        echo "📋 Useful commands:"
        echo "   Stop:     docker-compose down"
        echo "   Restart:  docker-compose restart"
        echo "   Logs:     docker-compose logs -f"
        echo "   Update:   docker-compose pull && docker-compose up --build -d"
    else
        echo "❌ Failed to start with docker-compose"
        exit 1
    fi
elif command -v docker &> /dev/null; then
    echo "🔧 Building and starting with Docker..."
    
    # Build the image
    docker build -t music-tools-suite .
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to build Docker image"
        exit 1
    fi
    
    # Create downloads directory if it doesn't exist
    mkdir -p downloads
    
    # Stop and remove existing container if it exists
    docker stop music-tools-suite 2>/dev/null
    docker rm music-tools-suite 2>/dev/null
    
    # Run the container
    docker run -d \
        --name music-tools-suite \
        -p 8501:8501 \
        -v "$(pwd)/downloads:/app/downloads" \
        --restart unless-stopped \
        music-tools-suite
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Music Tools Suite is running!"
        echo "🌐 Open your browser and go to: http://localhost:8501"
        echo ""
        echo "📋 Useful commands:"
        echo "   Stop:     docker stop music-tools-suite"
        echo "   Start:    docker start music-tools-suite"
        echo "   Restart:  docker restart music-tools-suite"
        echo "   Logs:     docker logs -f music-tools-suite"
        echo "   Remove:   docker stop music-tools-suite && docker rm music-tools-suite"
    else
        echo "❌ Failed to start Docker container"
        exit 1
    fi
else
    echo "❌ Neither docker nor docker-compose found"
    exit 1
fi

echo ""
echo "💡 Tips:"
echo "   - First startup may take a few minutes (downloading AI models)"
echo "   - Downloaded files will be saved to: $(pwd)/downloads"
echo "   - The app will automatically restart if it crashes" 