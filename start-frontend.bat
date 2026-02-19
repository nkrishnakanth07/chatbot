@echo off
echo ========================================
echo Starting Frontend...
echo ========================================
cd frontend

:: Check if node_modules exists
if not exist node_modules (
    echo ERROR: Dependencies not installed!
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo.
echo ✓ Starting React development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo The browser should open automatically
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm start
