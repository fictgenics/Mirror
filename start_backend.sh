#!/bin/bash

echo "🚀 Starting Mirror Backend Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy env.example to .env and configure your API keys"
    echo "   cp env.example .env"
    echo "   # Then edit .env with your API keys"
fi

# Start the server
echo "🌐 Starting FastAPI server..."
cd backend
python main.py
