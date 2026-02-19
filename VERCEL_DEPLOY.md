# 🚀 Deploy to Vercel - Complete Guide

## Prerequisites

1. **GitHub Account** - Sign up at https://github.com
2. **Vercel Account** - Sign up at https://vercel.com (use GitHub to sign in)
3. **OpenAI API Key** - Get from https://platform.openai.com/api-keys
4. **Pinecone Account** - Sign up at https://www.pinecone.io (free tier available)

---

## Why Pinecone Instead of ChromaDB?

**ChromaDB** stores data on the local filesystem, which doesn't work on Vercel's serverless functions (they're stateless).

**Pinecone** is a cloud-based vector database that's perfect for serverless deployments:
- ✅ Free tier: 1 index, 100K vectors
- ✅ Works perfectly with Vercel
- ✅ Fast and reliable
- ✅ No infrastructure to manage

---

## Step 1: Get Pinecone API Key (5 minutes)

1. **Sign up at Pinecone:**
   - Go to https://www.pinecone.io
   - Click "Sign Up" (free)
   - Verify your email

2. **Create an API Key:**
   - Log in to Pinecone console
   - Go to "API Keys" in the sidebar
   - Click "Create API Key"
   - Give it a name (e.g., "chatbot-vercel")
   - Copy the API key (starts with `pcsk_...` or similar)
   - **IMPORTANT:** Save this key - you won't see it again!

3. **Note your environment:**
   - In the Pinecone console, you'll see your environment (e.g., "us-east-1")
   - The code uses "us-east-1" by default
   - Free tier is typically in "gcp-starter" or "aws-starter"

---

## Step 2: Push Project to GitHub (5 minutes)

### Option A: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop:**
   - Go to https://desktop.github.com
   - Install and sign in with your GitHub account

2. **Add your project:**
   - Click "File" → "Add Local Repository"
   - Choose `D:\Projects\chatbot-project`
   - Click "Create a repository on GitHub"
   - Name it `chatbot-vercel`
   - Make it Public (so you can share the link)
   - Click "Publish repository"

### Option B: Using Command Line

1. **Open Command Prompt** in your project folder:
   ```bash
   cd D:\Projects\chatbot-project
   ```

2. **Initialize Git:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Vercel deployment"
   ```

3. **Create GitHub repo:**
   - Go to https://github.com/new
   - Name: `chatbot-vercel`
   - Make it Public
   - Don't initialize with README
   - Click "Create repository"

4. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/chatbot-vercel.git
   git branch -M main
   git push -u origin main
   ```

---

## Step 3: Deploy to Vercel (10 minutes)

### 3.1 Import Project

1. **Go to Vercel:**
   - Visit https://vercel.com
   - Click "Add New..." → "Project"

2. **Import Repository:**
   - You should see your `chatbot-vercel` repo
   - Click "Import"

### 3.2 Configure Project

**Framework Preset:** Vite (or leave as detected)

**Root Directory:** Leave as `.` (root)

**Build & Development Settings:**
- Leave defaults (Vercel auto-detects from vercel.json)

### 3.3 Add Environment Variables

Click "Environment Variables" and add these THREE variables:

**Variable 1:**
- **Name:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key (starts with `sk-...`)

**Variable 2:**
- **Name:** `PINECONE_API_KEY`
- **Value:** Your Pinecone API key

**Variable 3:**
- **Name:** `PINECONE_ENVIRONMENT`
- **Value:** Your Pinecone environment (e.g., `us-east-1`, `gcp-starter`)

**Apply to:** All Environments (Production, Preview, Development)

### 3.4 Deploy!

1. Click "Deploy"
2. Wait 3-5 minutes for the build
3. You'll see "Congratulations!" when done
4. Click "Visit" to see your live app! 🎉

Your app will be live at: `https://chatbot-vercel-xxx.vercel.app`

---

## Step 4: Test Your Deployment

1. **Visit your URL**
2. **Upload a PDF** (try a small one first, like a 1-2 page document)
3. **Ask a question** about the content
4. **Check for answers** with source citations

### If you see errors:

**Check the Vercel logs:**
1. Go to your Vercel dashboard
2. Click on your project
3. Click "Functions" tab
4. Look for errors in the logs

**Common issues:**
- API keys not set correctly
- Pinecone index not created (it auto-creates on first use)
- File too large (Vercel has 50MB limit)

---

## Step 5: Customize Your Deployment

### Add a Custom Domain (Optional)

**Free Option:**
Your Vercel URL is already pretty good: `chatbot-vercel.vercel.app`

**Custom Domain:**
1. Buy a domain from Namecheap (~$10/year)
2. In Vercel project settings → "Domains"
3. Add your domain
4. Update DNS settings as instructed
5. Wait for SSL certificate (automatic)

### Optimize Performance

**1. Adjust Pinecone Region:**
Edit `api/index.py` line with `ServerlessSpec`:
```python
spec=ServerlessSpec(cloud="aws", region="us-east-1")
```
Change to your nearest region for faster responses.

**2. Increase Timeout (if needed):**
Add to `vercel.json`:
```json
"functions": {
  "api/*.py": {
    "runtime": "python3.9",
    "maxDuration": 60
  }
}
```

---

## Understanding the Costs

### Vercel (Free Forever)
- ✅ 100 deployments/day
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN

### Pinecone (Free Tier)
- ✅ 1 serverless index
- ✅ 100,000 vectors (~100-200 documents)
- ✅ Good for portfolio/demo
- 💰 Paid: $70/month for more (only if you need it)

### OpenAI API (Pay-per-use)
- 📄 Embeddings: $0.0001 per 1K tokens
- 💬 GPT-4o-mini: $0.15/1M input, $0.60/1M output
- 📊 Estimate: $1-5/month for light demo use

**Total: ~$0-5/month** (just OpenAI for testing)

---

## Updating Your App

Every time you push to GitHub, Vercel automatically redeploys!

```bash
# Make your changes
cd D:\Projects\chatbot-project

# Commit and push
git add .
git commit -m "Updated feature X"
git push

# Vercel auto-deploys in ~2 minutes
```

---

## Troubleshooting

### "Build Failed"

**Check build logs:**
1. Vercel dashboard → Your project → Deployments
2. Click the failed deployment
3. Check "Building" logs

**Common fixes:**
- Missing dependency in requirements.txt
- Syntax error in code
- Wrong Python version

### "API Returns 500 Error"

**Check function logs:**
1. Vercel dashboard → Your project → Functions
2. Click on `/api/index`
3. View recent invocations

**Common fixes:**
- API keys not set
- Pinecone index not accessible
- Timeout (increase maxDuration)

### "Upload Takes Too Long"

Vercel has limits:
- 50MB file size max
- 60 second timeout (can extend to 300s on Pro)

**Solutions:**
- Use smaller PDFs for testing
- Split large documents
- Upgrade to Vercel Pro if needed

### "Pinecone Index Error"

**Check your Pinecone console:**
1. Verify index was created
2. Check your API key is correct
3. Verify environment matches

**Force create index manually:**
1. Go to Pinecone console
2. Create index named `chatbot-docs`
3. Dimensions: 1536
4. Metric: cosine

---

## Production Best Practices

### 1. Add Rate Limiting

```python
# In api/index.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat/{session_id}")
@limiter.limit("10/minute")
async def chat(...):
    pass
```

### 2. Add Analytics

```python
# Track usage
import posthog

posthog.capture(
    distinct_id=session_id,
    event='chat_message',
    properties={'question_length': len(question)}
)
```

### 3. Add Error Monitoring

Use Vercel's built-in monitoring or add Sentry:

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## Sharing Your Project

### On LinkedIn:

```
🚀 Just deployed my Multi-Document RAG Chatbot!

Built with:
• FastAPI + Vercel Serverless Functions
• LangChain for RAG pipeline
• OpenAI GPT-4 for AI responses
• Pinecone for vector storage
• React for the frontend

Try it: https://your-app.vercel.app
Code: https://github.com/your-username/chatbot-vercel

#AI #MachineLearning #RAG #Serverless #LangChain #OpenAI
```

### On Your Resume:

```
Multi-Document RAG Chatbot | FastAPI, LangChain, OpenAI, Pinecone, React
• Built full-stack serverless AI chatbot supporting multiple document uploads
• Implemented RAG (Retrieval Augmented Generation) for context-aware responses
• Deployed on Vercel with automatic scaling and global CDN
• Live demo: https://your-app.vercel.app | Code: github.com/you/chatbot
```

---

## What You've Accomplished

✅ **Deployed a production AI application**
✅ **Learned serverless architecture**
✅ **Worked with vector databases**
✅ **Implemented RAG (cutting-edge AI technique)**
✅ **Created a portfolio-worthy project**
✅ **No ongoing costs** (free tier)
✅ **Automatic HTTPS & CDN**
✅ **Auto-scaling** (handles traffic spikes)

---

## Next Steps

### For Your Portfolio:
1. ✅ Add project to resume
2. ✅ Write a blog post about building it
3. ✅ Share on LinkedIn
4. ✅ Add to your GitHub profile README

### For Learning:
1. Add user authentication
2. Support more file types
3. Add conversation export
4. Implement caching for common queries

### For Production:
1. Add rate limiting
2. Implement usage tracking
3. Add error monitoring
4. Set up alerts

---

## Support

**Vercel Documentation:**
- https://vercel.com/docs

**Pinecone Documentation:**
- https://docs.pinecone.io

**Questions?**
- Vercel has a great community Discord
- Pinecone has excellent docs and support

---

🎉 **Congratulations!** Your app is now live and accessible worldwide!

Share the link proudly - you've built something impressive! 🚀
