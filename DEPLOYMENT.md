# 🚀 Deployment Guide

Complete guide to deploying your Multi-Document RAG Chatbot for free.

## Overview

We'll use:
- **Render.com** for backend (Free tier: 750 hours/month)
- **Vercel** for frontend (Free tier: unlimited personal projects)

Total cost: **$0/month** ✨

## Prerequisites

1. GitHub account
2. OpenAI API key
3. Git installed locally

## Part 1: Prepare Your Code

### 1. Initialize Git Repository

```bash
cd chatbot-project
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repository

1. Go to GitHub.com
2. Click "New repository"
3. Name it `chatbot-project`
4. Don't initialize with README (we already have one)
5. Copy the commands to push existing repo

```bash
git remote add origin https://github.com/YOUR_USERNAME/chatbot-project.git
git branch -M main
git push -u origin main
```

## Part 2: Deploy Backend (Render.com)

### 1. Sign Up / Log In

Go to [render.com](https://render.com) and sign up with GitHub

### 2. Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account if not already connected
3. Select your `chatbot-project` repository
4. Click "Connect"

### 3. Configure Service

Fill in the following:

**Name**: `chatbot-api` (or any name you prefer)

**Region**: Choose closest to you

**Branch**: `main`

**Root Directory**: `backend`

**Runtime**: `Python 3`

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type**: `Free`

### 4. Add Environment Variables

Scroll down to "Environment Variables" and add:

**Key**: `OPENAI_API_KEY`
**Value**: `sk-your-openai-api-key-here`

### 5. Deploy

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your backend will be live at: `https://chatbot-api.onrender.com` (or your chosen name)
4. Test it by visiting: `https://your-app.onrender.com/health`

**⚠️ Important Notes:**
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- For production, upgrade to paid tier ($7/month) for always-on service

## Part 3: Deploy Frontend (Vercel)

### 1. Sign Up / Log In

Go to [vercel.com](https://vercel.com) and sign up with GitHub

### 2. Import Project

1. Click "Add New..." → "Project"
2. Import your `chatbot-project` repository
3. Click "Import"

### 3. Configure Project

**Framework Preset**: `Create React App` (auto-detected)

**Root Directory**: Click "Edit" and select `frontend`

**Build Command**: `npm run build` (auto-filled)

**Output Directory**: `build` (auto-filled)

### 4. Add Environment Variable

Click "Environment Variables" and add:

**Name**: `REACT_APP_API_URL`
**Value**: `https://your-render-app.onrender.com` (your backend URL from Step 2)

### 5. Deploy

1. Click "Deploy"
2. Wait 2-3 minutes
3. Your frontend will be live at: `https://your-project.vercel.app`

## Part 4: Test Your Application

1. Visit your Vercel URL
2. Wait for backend to wake up (first visit may take a minute)
3. Upload a PDF document
4. Ask questions!

## Updating Your Application

### Update Backend

```bash
cd backend
# Make your changes
git add .
git commit -m "Update backend"
git push
```

Render will automatically redeploy.

### Update Frontend

```bash
cd frontend
# Make your changes
git add .
git commit -m "Update frontend"
git push
```

Vercel will automatically redeploy.

## Alternative: Netlify for Frontend

If you prefer Netlify over Vercel:

### 1. Sign Up

Go to [netlify.com](https://netlify.com) and sign up with GitHub

### 2. New Site

1. Click "Add new site" → "Import an existing project"
2. Choose GitHub and select your repo
3. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

### 3. Environment Variables

1. Go to "Site settings" → "Environment variables"
2. Add: `REACT_APP_API_URL` = your Render backend URL

### 4. Deploy

Click "Deploy site"

## Troubleshooting

### Backend Issues

**Problem**: Backend doesn't wake up
**Solution**: Visit the `/health` endpoint directly to wake it up

**Problem**: "Module not found" errors
**Solution**: Check that `requirements.txt` includes all dependencies

**Problem**: Database errors
**Solution**: Make sure ChromaDB directory is not in `.gitignore`

### Frontend Issues

**Problem**: Can't connect to backend
**Solution**: Check CORS settings in `main.py` and API URL in frontend `.env`

**Problem**: Build fails
**Solution**: Make sure all dependencies are in `package.json`

**Problem**: Environment variables not working
**Solution**: In React, they must start with `REACT_APP_`

### CORS Issues

If you get CORS errors, make sure your backend `main.py` has:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel/Netlify
- [ ] Environment variables set correctly
- [ ] Test uploading a document
- [ ] Test asking questions
- [ ] Test multiple documents
- [ ] Verify source citations work
- [ ] Test on mobile device
- [ ] Share with friends!

## Cost Optimization

**Free Tier Limits:**
- Render: 750 hours/month (one always-on app)
- Vercel: Unlimited bandwidth, 100GB bandwidth/month
- OpenAI: Pay per token (estimate: $0.50-$2/month for moderate use)

**To Stay Free:**
- Use GPT-4o-mini (cheaper) instead of GPT-4
- Implement caching for repeated queries
- Set up request limits
- Monitor OpenAI usage dashboard

## Next Steps

1. **Add Authentication**: Implement user login
2. **Add Database**: Use PostgreSQL for persistent sessions
3. **Monitor Usage**: Set up logging and analytics
4. **Custom Domain**: Add your own domain name
5. **SEO**: Optimize for search engines

## Support

If you run into issues:
1. Check the logs on Render/Vercel
2. Review the main README.md
3. Check CORS and environment variables
4. Test backend independently at `/health` endpoint

---

🎉 Congratulations! Your chatbot is now live and accessible to the world!

Share it on:
- LinkedIn (great for your portfolio!)
- Twitter/X
- Your resume
- GitHub README

Remember to mention:
- Multi-document RAG capabilities
- Session management
- Real-time AI responses
- Clean, modern UI
- Free deployment
