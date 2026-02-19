# 🚀 Quick Start Guide

## For Windows Users

### First Time Setup (5 minutes)

1. **Get OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-...`)

2. **Run Setup**
   ```
   Double-click: setup.bat
   ```
   Wait for it to complete.

3. **Add API Key**
   - Open `backend\.env` in Notepad
   - Replace `your_openai_api_key_here` with your actual key
   - Save and close

4. **Start Backend** (in one terminal)
   ```
   Double-click: start-backend.bat
   ```
   Wait until you see "Application startup complete"

5. **Start Frontend** (in another terminal)
   ```
   Double-click: start-frontend.bat
   ```
   Browser will open automatically at http://localhost:3000

## For Mac/Linux Users

### First Time Setup (5 minutes)

1. **Get OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key

2. **Run Setup**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Add API Key**
   ```bash
   nano backend/.env
   # Replace your_openai_api_key_here with your key
   # Press Ctrl+X, then Y, then Enter to save
   ```

4. **Start Backend** (in one terminal)
   ```bash
   ./start-backend.sh
   ```

5. **Start Frontend** (in another terminal)
   ```bash
   ./start-frontend.sh
   ```

## Using the Application

### Step 1: Upload Documents
1. Click "📎 Upload PDF Document"
2. Select one or more PDF files
3. Wait for "✅ Document uploaded!"

### Step 2: Ask Questions
1. Type your question in the input box
2. Press Enter or click "📤 Send"
3. View the AI's response with sources

### Step 3: Manage Documents
1. Click "📚 Documents" to view uploaded files
2. Click 🗑️ next to a document to remove it
3. Click "🔄 New Session" to start fresh

## Common Issues & Solutions

### "Module not found" Error
**Problem:** Missing dependencies
**Solution:** Run `setup.bat` (or `setup.sh`) again

### "OpenAI API Error"
**Problem:** Invalid API key or no credits
**Solution:** 
- Check your API key in `backend/.env`
- Verify you have credits at https://platform.openai.com/account/usage

### "Cannot connect to backend"
**Problem:** Backend not running or wrong URL
**Solution:**
- Make sure backend is running (should see in terminal)
- Check `frontend/.env` has correct URL: `http://localhost:8000`

### Backend "sleeps" on Render
**Problem:** Free tier goes to sleep after 15 min
**Solution:** First request will take 30-60 seconds to wake up (this is normal)

### CORS Error
**Problem:** Frontend can't access backend
**Solution:** Make sure both are running and on correct ports

## Port Reference

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/docs

## File Structure Quick Reference

```
chatbot-project/
├── backend/
│   ├── main.py          ← Main backend code
│   ├── .env             ← Your API key goes here
│   └── requirements.txt ← Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js       ← Main React component
│   │   └── App.css      ← Styling
│   └── .env             ← Backend URL
├── setup.bat/.sh        ← Run this first
├── start-backend.bat/.sh
└── start-frontend.bat/.sh
```

## Development Tips

### Making Changes

**Backend Changes:**
1. Edit files in `backend/`
2. Restart backend server (Ctrl+C, then run start-backend again)

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Changes apply automatically (no restart needed)

### Adding New Features

**New API Endpoint:**
1. Add function to `backend/main.py`
2. Decorate with `@app.post("/your-endpoint")`
3. Use in frontend with `axios.post()`

**New UI Component:**
1. Add to `frontend/src/App.js`
2. Style in `frontend/src/App.css`

## Testing Checklist

Before deploying, test these:

- [ ] Upload a single PDF
- [ ] Ask a question
- [ ] Upload multiple PDFs
- [ ] Ask questions about multiple documents
- [ ] View sources
- [ ] Delete a document
- [ ] Start new session
- [ ] Test on mobile (if deployed)

## Next Steps

### For Portfolio

1. **Deploy it** - Follow DEPLOYMENT.md
2. **Add to Resume**
   - Link to live demo
   - Link to GitHub repo
   - Mention: RAG, OpenAI, LangChain, FastAPI, React

3. **LinkedIn Post**
   ```
   🚀 Just built a Multi-Document RAG Chatbot!
   
   Features:
   ✅ Upload multiple PDFs
   ✅ Ask questions across all documents
   ✅ Get answers with source citations
   ✅ Session-based conversations
   
   Tech: FastAPI, LangChain, OpenAI GPT-4, ChromaDB, React
   
   Try it: [your-deployed-url]
   Code: [your-github-url]
   
   #AI #MachineLearning #RAG #OpenAI #LangChain
   ```

### For Learning

1. **Understand the code**
   - Read ARCHITECTURE.md
   - Add console.log() to see data flow
   - Try modifying prompts

2. **Add features**
   - User authentication
   - More file types (Word, TXT)
   - Export conversations
   - Voice input

3. **Improve performance**
   - Add caching
   - Implement streaming
   - Optimize chunk sizes

## Getting Help

1. **Check the docs**
   - README.md - Full documentation
   - ARCHITECTURE.md - How it works
   - DEPLOYMENT.md - Deploy to production

2. **Debug**
   - Check terminal output for errors
   - Use browser DevTools (F12)
   - Check backend logs

3. **Common Resources**
   - LangChain docs: https://python.langchain.com
   - FastAPI docs: https://fastapi.tiangolo.com
   - React docs: https://react.dev

## Cost Tracking

### Monitor OpenAI Usage
1. Go to https://platform.openai.com/usage
2. Set up usage alerts
3. Check daily spending

### Estimate
- Development: ~$1-2/day
- Light production: ~$30-50/month
- Use GPT-4o-mini for lower costs

## Maintenance

### Weekly
- [ ] Check OpenAI usage/costs
- [ ] Review error logs
- [ ] Update dependencies if needed

### Monthly
- [ ] Clear old ChromaDB data
- [ ] Review and optimize slow queries
- [ ] Update to latest LangChain version

---

🎉 You're all set! Happy coding!

For questions or issues, check the full README.md or ARCHITECTURE.md
