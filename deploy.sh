#!/bin/bash

echo "========================================"
echo "Automated GitHub Deployment"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo ""
fi

# Get user input
echo "Enter your GitHub username:"
read GITHUB_USER
echo ""

echo "Enter your repository name (e.g., chatbot-vercel):"
read REPO_NAME
echo ""

# Add all files
echo "Adding files to Git..."
git add .
echo ""

# Commit changes
echo "Enter commit message (or press Enter for default):"
read COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update project"
fi

git commit -m "$COMMIT_MSG"
echo ""

# Check if remote exists
if ! git remote -v | grep -q origin; then
    echo "Setting up GitHub remote..."
    git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
    echo ""
    echo "Remote added: https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo ""
    echo "IMPORTANT: Make sure you've created this repository on GitHub first!"
    echo "Visit: https://github.com/new"
    echo ""
    read -p "Press Enter to continue..."
fi

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Success! Code pushed to GitHub"
    echo "========================================"
    echo ""
    echo "Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "Next Steps:"
    echo "1. Go to https://vercel.com/new"
    echo "2. Import your GitHub repository"
    echo "3. Add environment variables (see below)"
    echo "4. Click Deploy!"
    echo ""
    echo "========================================"
    echo "Environment Variables for Vercel:"
    echo "========================================"
    echo "OPENAI_API_KEY = your OpenAI key"
    echo "PINECONE_API_KEY = your Pinecone key"
    echo "PINECONE_ENVIRONMENT = us-east-1"
    echo "========================================"
    echo ""
else
    echo ""
    echo "========================================"
    echo "Push failed! Common solutions:"
    echo "========================================"
    echo "1. Make sure the repository exists on GitHub"
    echo "2. Check your GitHub credentials"
    echo "3. You may need to authenticate with GitHub CLI:"
    echo "   gh auth login"
    echo ""
    echo "Or use a Personal Access Token:"
    echo "   https://github.com/settings/tokens"
    echo "========================================"
    echo ""
fi
