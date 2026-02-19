#!/bin/bash

echo "========================================"
echo "Multi-Document RAG Chatbot Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 16+ from nodejs.org"
    exit 1
fi

echo "✓ Python found"
echo "✓ Node.js found"
echo ""

# Backend Setup
echo "========================================"
echo "Setting up Backend..."
echo "========================================"
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY"
    echo ""
fi

cd ..

# Frontend Setup
echo "========================================"
echo "Setting up Frontend..."
echo "========================================"
cd frontend

echo "Installing dependencies..."
npm install

echo ""
echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created frontend/.env"
fi

cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Edit backend/.env and add your OPENAI_API_KEY"
echo "2. Run ./start-backend.sh to start the backend server"
echo "3. Run ./start-frontend.sh to start the frontend"
echo ""
echo "For detailed instructions, see README.md"
echo "========================================"
