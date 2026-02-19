@echo off
echo ========================================
echo Automated GitHub Deployment
echo ========================================
echo.

:: Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

:: Get user input for GitHub repo
echo Enter your GitHub username:
set /p GITHUB_USER=
echo.

echo Enter your repository name (e.g., chatbot-vercel):
set /p REPO_NAME=
echo.

:: Add all files
echo Adding files to Git...
git add .
echo.

:: Commit changes
echo Enter commit message (or press Enter for default):
set /p COMMIT_MSG=
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update project

git commit -m "%COMMIT_MSG%"
echo.

:: Check if remote exists
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo Setting up GitHub remote...
    git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
    echo.
    echo Remote added: https://github.com/%GITHUB_USER%/%REPO_NAME%.git
    echo.
    echo IMPORTANT: Make sure you've created this repository on GitHub first!
    echo Visit: https://github.com/new
    echo.
    pause
)

:: Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo Push failed! Common solutions:
    echo ========================================
    echo 1. Make sure the repository exists on GitHub
    echo 2. Check your GitHub credentials
    echo 3. You may need to authenticate with GitHub CLI:
    echo    gh auth login
    echo.
    echo Or use a Personal Access Token:
    echo    https://github.com/settings/tokens
    echo ========================================
    pause
) else (
    echo.
    echo ========================================
    echo Success! Code pushed to GitHub
    echo ========================================
    echo.
    echo Repository: https://github.com/%GITHUB_USER%/%REPO_NAME%
    echo.
    echo Next Steps:
    echo 1. Go to https://vercel.com/new
    echo 2. Import your GitHub repository
    echo 3. Add environment variables (see below)
    echo 4. Click Deploy!
    echo.
    echo ========================================
    echo Environment Variables for Vercel:
    echo ========================================
    echo OPENAI_API_KEY = your OpenAI key
    echo PINECONE_API_KEY = your Pinecone key
    echo PINECONE_ENVIRONMENT = us-east-1
    echo ========================================
    echo.
    pause
)
