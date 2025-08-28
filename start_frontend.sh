#!/bin/bash

echo "🎨 Starting Mirror Frontend Development Server..."

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "✅ Dependencies already installed"
fi

# Start the development server
echo "🌐 Starting React development server..."
cd frontend
npm start
