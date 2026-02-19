@echo off
echo ========================================
echo Starting Backend Server...
echo ========================================
cd backend

:: Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your OPENAI_API_KEY
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo ✓ Virtual environment activated
echo ✓ Starting FastAPI server...
echo.
echo Backend will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python main.py
