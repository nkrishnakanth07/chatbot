@echo off
echo ========================================
echo Multi-Document RAG Chatbot Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from nodejs.org
    pause
    exit /b 1
)

echo ✓ Python found
echo ✓ Node.js found
echo.

:: Backend Setup
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit backend\.env and add your OPENAI_API_KEY
    echo.
)

cd ..

:: Frontend Setup
echo ========================================
echo Setting up Frontend...
echo ========================================
cd frontend

echo Installing dependencies...
call npm install

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo ✓ Created frontend\.env
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Edit backend\.env and add your OPENAI_API_KEY
echo 2. Run start-backend.bat to start the backend server
echo 3. Run start-frontend.bat to start the frontend
echo.
echo For detailed instructions, see README.md
echo ========================================
pause
