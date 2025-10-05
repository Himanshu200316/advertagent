#!/bin/bash

# Instagram Advertisement Agent Deployment Script

set -e

echo "🚀 Starting Instagram Advertisement Agent Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your actual API credentials before running again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data generated_images logs

# Set permissions
echo "🔐 Setting permissions..."
chmod +x instagram_agent.py
chmod +x deploy.sh

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if container is running
if docker-compose ps | grep -q "instagram-agent.*Up"; then
    echo "✅ Instagram Advertisement Agent is running successfully!"
    echo ""
    echo "📊 Useful commands:"
    echo "  View logs: docker-compose logs -f instagram-agent"
    echo "  Manual posting: docker-compose exec instagram-agent python instagram_agent.py manual"
    echo "  View analytics: docker-compose exec instagram-agent python instagram_agent.py analytics"
    echo "  Stop services: docker-compose down"
    echo ""
    echo "🕐 The agent will automatically post daily at 12 AM (00:00)"
else
    echo "❌ Failed to start Instagram Advertisement Agent"
    echo "📋 Check logs: docker-compose logs instagram-agent"
    exit 1
fi