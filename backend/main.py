from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionResponse(BaseModel):
    session_id: str
    message: str

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/session/create")
async def create_session():
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }

@app.post("/api/upload/{session_id}")
async def upload_placeholder(session_id: str):
    """Placeholder for document upload"""
    return {
        "message": "Upload endpoint - AI features coming soon!",
        "session_id": session_id,
        "doc_id": str(uuid.uuid4()),
        "chunks": 0
    }

@app.post("/api/chat/{session_id}")
async def chat_placeholder(session_id: str):
    """Placeholder for chat"""
    return {
        "answer": "🎉 Success! Your frontend and backend are connected! AI features will be added next.",
        "sources": []
    }