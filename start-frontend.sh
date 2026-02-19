#!/bin/bash

echo "========================================"
echo "Starting Frontend..."
echo "========================================"
cd frontend

# Check if node_modules exists
if [ ! -d node_modules ]; then
    echo "ERROR: Dependencies not installed!"
    echo "Please run ./setup.sh first"
    exit 1
fi

echo ""
echo "✓ Starting React development server..."
echo ""
echo "Frontend will be available at: http://localhost:3000"
echo "The browser should open automatically"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

npm start
