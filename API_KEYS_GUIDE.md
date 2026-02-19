# 🔑 API Keys Setup Guide

## Where to Enter Your API Keys

### 📍 Quick Answer

**For LOCAL Development:**
- OpenAI Key → `backend/.env` file

**For VERCEL Deployment:**
- OpenAI Key → Vercel Dashboard → Environment Variables
- Pinecone Key → Vercel Dashboard → Environment Variables

**For RENDER Deployment:**
- OpenAI Key → Render Dashboard → Environment Variables

---

## 🏠 Local Development Setup

### Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Name it (e.g., "Chatbot Local Dev")
5. Copy the key (starts with `sk-...`)
6. ⚠️ **IMPORTANT:** Save it somewhere safe - you won't see it again!

### Step 2: Add to Local Environment

**Option A: Using the .env file (Recommended)**

1. Navigate to your backend folder:
   ```
   D:\Projects\chatbot-project\backend
   ```

2. Copy `.env.example` to `.env`:
   ```bash
   # Windows Command Prompt
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

3. Open `.env` in Notepad or any text editor:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-abc123xyz...
   ```

5. Save and close the file

---

## ☁️ Vercel Deployment Setup

### Step 1: Get Your API Keys

**OpenAI:**
- Already have it from above ✓

**Pinecone:**
1. Go to https://www.pinecone.io
2. Sign up (free tier available)
3. Verify email
4. Go to "API Keys" in sidebar
5. Click "Create API Key"
6. Name it (e.g., "Chatbot Vercel")
7. Copy the key

### Step 2: Add to Vercel Dashboard

When deploying to Vercel, you'll add 3 environment variables:

**Variable 1 - OpenAI:**
- **Name:** `OPENAI_API_KEY`
- **Value:** `sk-proj-abc123xyz...` (your OpenAI key)

**Variable 2 - Pinecone:**
- **Name:** `PINECONE_API_KEY`
- **Value:** (your Pinecone key)

**Variable 3 - Pinecone Environment:**
- **Name:** `PINECONE_ENVIRONMENT`
- **Value:** `us-east-1` (or your Pinecone region)

---

## 🎨 Render Deployment Setup

When deploying to Render, add this environment variable:

**OpenAI Key:**
- **Key:** `OPENAI_API_KEY`
- **Value:** `sk-proj-abc123xyz...`

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Keep API keys in `.env` files (local development)
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Use environment variables in deployment platforms
- ✅ Regenerate keys if accidentally exposed

### ❌ DON'T:
- ❌ Never commit `.env` files to Git
- ❌ Never hardcode keys in source code
- ❌ Never share keys in chat/email
- ❌ Never post screenshots with visible keys

---

## 🧪 Verify Your Setup

### Test Local Setup:

```bash
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key found!' if os.getenv('OPENAI_API_KEY') else 'Key NOT found!')"
```

Should print: `Key found!`

---

## 📋 Quick Reference

| Environment | Where to Add Keys |
|-------------|-------------------|
| **Local Dev** | `backend/.env` file |
| **Vercel** | Vercel Dashboard → Environment Variables |
| **Render** | Render Dashboard → Environment tab |

---

Remember: **NEVER commit your `.env` file to Git!** It's already in `.gitignore`.
