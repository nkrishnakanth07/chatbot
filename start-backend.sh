#!/bin/bash

echo "========================================"
echo "Starting Backend Server..."
echo "========================================"
cd backend

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and add your OPENAI_API_KEY"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "✓ Virtual environment activated"
echo "✓ Starting FastAPI server..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python main.py
