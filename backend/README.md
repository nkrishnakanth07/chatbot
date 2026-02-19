# Multi-Document RAG Chatbot Backend

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=sk-...
```

4. Run the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /session/create` - Create a new chat session
- `POST /upload/{session_id}` - Upload a PDF document to a session
- `POST /chat/{session_id}` - Send a message and get a response
- `GET /session/{session_id}/history` - Get conversation history
- `GET /session/{session_id}/documents` - Get all documents in session
- `DELETE /session/{session_id}/document/{doc_id}` - Remove a document
- `DELETE /session/{session_id}` - Delete entire session
- `GET /health` - Health check

## Features

- ✅ Multi-document support per session
- ✅ Conversation history tracking
- ✅ Session-based isolation
- ✅ Source citations with document references
- ✅ OpenAI GPT-4 integration
- ✅ ChromaDB vector storage

## Deployment

### Render.com
1. Push to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY`
