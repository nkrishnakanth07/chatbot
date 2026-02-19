# 🚀 Installation Instructions for D:\Projects\Claude Chatbot

## Method 1: Extract Zip File (Recommended)

1. **Download the zip file** I've provided
2. **Extract to your desired location:**
   - Right-click on `chatbot-project.zip`
   - Select "Extract All..."
   - Choose `D:\Projects\` as the destination
   - Click "Extract"
   - You should now have `D:\Projects\chatbot-project\`

3. **Get your OpenAI API Key:**
   - Go to https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Give it a name (e.g., "Chatbot Project")
   - Copy the key (starts with `sk-...`) - you won't see it again!

4. **Run the setup script:**
   - Open `D:\Projects\chatbot-project`
   - Double-click `setup.bat`
   - Wait for it to complete (5-10 minutes)
   - It will install all dependencies

5. **Add your API key:**
   - Open `D:\Projects\chatbot-project\backend\.env` in Notepad
   - Replace `your_openai_api_key_here` with your actual API key
   - Save and close

6. **Start the application:**
   - Open TWO command prompt windows
   
   **Window 1 (Backend):**
   - Navigate to: `cd D:\Projects\chatbot-project`
   - Run: `start-backend.bat`
   - Wait until you see "Application startup complete"
   
   **Window 2 (Frontend):**
   - Navigate to: `cd D:\Projects\chatbot-project`
   - Run: `start-frontend.bat`
   - Browser will open automatically at http://localhost:3000

## Method 2: Manual Setup (If Method 1 Fails)

If the automated setup doesn't work, follow these steps:

### Backend Setup

1. **Open Command Prompt** and navigate:
   ```
   cd D:\Projects\chatbot-project\backend
   ```

2. **Create virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key

### Frontend Setup

1. **Open another Command Prompt** and navigate:
   ```
   cd D:\Projects\chatbot-project\frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Create .env file:**
   - Copy `.env.example` to `.env`
   - Should contain: `REACT_APP_API_URL=http://localhost:8000`

### Start the Application

**Terminal 1 (Backend):**
```
cd D:\Projects\chatbot-project\backend
venv\Scripts\activate
python main.py
```

**Terminal 2 (Frontend):**
```
cd D:\Projects\chatbot-project\frontend
npm start
```

## Troubleshooting

### "Python not found"
**Solution:** 
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal

### "Node not found"
**Solution:**
- Install Node.js from https://nodejs.org
- Download the LTS (Long Term Support) version
- Restart your terminal

### "pip install fails"
**Solution:**
- Make sure virtual environment is activated
- Try: `python -m pip install --upgrade pip`
- Then retry: `pip install -r requirements.txt`

### "npm install fails"
**Solution:**
- Delete `node_modules` folder if it exists
- Delete `package-lock.json` if it exists
- Run `npm install` again

### "Can't connect to backend"
**Solution:**
- Make sure backend is running (check terminal for errors)
- Verify backend is at http://localhost:8000
- Check `frontend\.env` has correct URL

### "OpenAI API Error"
**Solution:**
- Verify API key is correct in `backend\.env`
- Check you have credits at https://platform.openai.com/usage
- Make sure key starts with `sk-`

## What's Included in the Project

```
D:\Projects\chatbot-project\
├── backend/              # FastAPI backend
│   ├── main.py          # Main application code
│   ├── requirements.txt # Python dependencies
│   └── .env.example     # Template for your API key
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.js      # Main React component
│   │   └── App.css     # Styles
│   ├── package.json    # Node dependencies
│   └── .env.example    # Template for backend URL
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick reference guide
├── DEPLOYMENT.md       # How to deploy online
├── TUTORIAL.md         # Complete learning guide
├── ARCHITECTURE.md     # How everything works
├── setup.bat           # Automated setup (Windows)
├── setup.sh            # Automated setup (Mac/Linux)
├── start-backend.bat   # Start backend (Windows)
├── start-frontend.bat  # Start frontend (Windows)
└── And more...
```

## Next Steps After Installation

1. **Test the application:**
   - Upload a PDF document
   - Ask a question about it
   - Upload another PDF
   - Ask questions about both documents

2. **Read the documentation:**
   - Start with `QUICKSTART.md` for basics
   - Read `TUTORIAL.md` to understand the code
   - Check `ARCHITECTURE.md` to see how it all works

3. **Deploy it online:**
   - Follow `DEPLOYMENT.md` to put it on the internet
   - Free hosting on Render + Vercel

4. **Add it to your portfolio:**
   - Deploy it publicly
   - Add to your GitHub
   - Link from your resume/LinkedIn

## Support

If you run into any issues:

1. **Check the logs:**
   - Backend errors appear in the backend terminal
   - Frontend errors appear in browser console (F12)

2. **Read the docs:**
   - `QUICKSTART.md` for common issues
   - `README.md` for full documentation

3. **Common fixes:**
   - Restart both backend and frontend
   - Check API key is correct
   - Verify both servers are running
   - Clear browser cache

## Quick Test

To verify everything works:

1. Start backend and frontend
2. Browser opens to http://localhost:3000
3. Click "Upload PDF Document"
4. Upload any PDF file
5. Wait for "Document uploaded" message
6. Type: "What is this document about?"
7. Press Enter
8. You should see an AI response with sources

If all steps work: ✅ Success! You're ready to go!

## Getting Help

- Check `QUICKSTART.md` for quick answers
- Read `TUTORIAL.md` for detailed explanations
- Check `ARCHITECTURE.md` to understand the system
- Review error messages in terminal/browser console

---

🎉 Congratulations on setting up your Multi-Document RAG Chatbot!

This is a production-ready application you can:
- Use for your own documents
- Deploy online for free
- Add to your portfolio
- Show to potential employers
- Build upon with new features

Have fun building! 🚀
