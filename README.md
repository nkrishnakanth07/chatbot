# 📄 Multi-Document RAG Chatbot

A full-stack chatbot application that allows users to upload multiple PDF documents and ask questions across all of them. Built with FastAPI, LangChain, OpenAI, ChromaDB, and React.

## 🌟 Features

### Backend
- ✅ **Multi-document support** - Upload and query multiple PDFs in a single session
- ✅ **Conversation history** - Maintains context across multiple questions
- ✅ **Session management** - Isolated sessions for different users/contexts
- ✅ **Source citations** - References specific documents and passages
- ✅ **Vector search** - Fast semantic search using ChromaDB
- ✅ **OpenAI GPT-4** - Powered by state-of-the-art language models

### Frontend
- ✅ **Modern React UI** - Clean, responsive interface
- ✅ **Document management** - View, upload, and delete documents
- ✅ **Real-time chat** - Smooth conversation experience
- ✅ **Source viewing** - Click to see where answers came from
- ✅ **Session persistence** - Continue conversations across page refreshes
- ✅ **Beautiful animations** - Polished user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

5. Run the server:
```bash
python main.py
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm start
```

Frontend will open at `http://localhost:3000`

## 📁 Project Structure

```
chatbot-project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── README.md            # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styles
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── package.json         # Node dependencies
│   ├── .env.example         # Environment variables template
│   └── README.md            # Frontend documentation
└── README.md                # This file
```

## 🔧 API Endpoints

### Session Management
- `POST /session/create` - Create a new chat session
- `GET /session/{session_id}/history` - Get conversation history
- `GET /session/{session_id}/documents` - List all documents
- `DELETE /session/{session_id}` - Delete a session

### Document Management
- `POST /upload/{session_id}` - Upload a PDF document
- `DELETE /session/{session_id}/document/{doc_id}` - Remove a document

### Chat
- `POST /chat/{session_id}` - Send a message and get response

### Health
- `GET /health` - Check API status

## 🌐 Deployment

### Backend (Render.com - Free Tier)

1. Push your code to GitHub

2. Go to [render.com](https://render.com) and create a new Web Service

3. Connect your GitHub repository

4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable**: `OPENAI_API_KEY` = your API key

5. Deploy! Your backend will be live at `https://your-app.onrender.com`

### Frontend (Vercel - Free Tier)

1. Push your frontend code to GitHub

2. Go to [vercel.com](https://vercel.com) and import your project

3. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Environment Variable**: `REACT_APP_API_URL` = your Render backend URL

4. Deploy! Your frontend will be live at `https://your-app.vercel.app`

### Alternative: Netlify for Frontend

1. Push to GitHub
2. Create new site from Git on [netlify.com](https://netlify.com)
3. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
   - **Environment**: `REACT_APP_API_URL` = your backend URL
4. Deploy!

## 💡 Usage Tips

1. **Start a new session** when switching topics or document sets
2. **Upload related documents** to a single session for cross-document queries
3. **Check sources** to verify where information came from
4. **Clear sessions** regularly to save on vector storage

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM application framework
- **OpenAI GPT-4** - Language model
- **ChromaDB** - Vector database
- **PyPDF** - PDF text extraction

### Frontend
- **React** - UI library
- **Axios** - HTTP client
- **CSS3** - Styling with animations

## 🔐 Security Notes

- Never commit `.env` files with API keys
- Use environment variables for all sensitive data
- Consider adding authentication for production use
- Implement rate limiting on the API

## 📝 License

MIT License - feel free to use this project for your portfolio!

## 🤝 Contributing

This is a portfolio project, but feel free to fork and customize for your needs!

## 📧 Support

For issues or questions, please open a GitHub issue.

## 🎯 Future Enhancements

- [ ] User authentication
- [ ] Persistent database for sessions
- [ ] Support for more file types (Word, TXT, etc.)
- [ ] Advanced document preprocessing
- [ ] Export conversation history
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Mobile app version

---

Built with ❤️ using OpenAI, LangChain, FastAPI, and React
