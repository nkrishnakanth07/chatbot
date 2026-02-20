from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="Multi-Document RAG Chatbot")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    question: str
    chat_history: List[dict] = []

class SessionResponse(BaseModel):
    session_id: str
    message: str

@app.get("/")
async def root():
    return {"message": "Multi-Document RAG Chatbot API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/session/create", response_model=SessionResponse)
async def create_new_session():
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "documents": [],
        "chat_history": []
    }
    return SessionResponse(
        session_id=session_id,
        message="Session created successfully"
    )

@app.post("/api/upload/{session_id}")
async def upload_document(session_id: str, file: UploadFile = File(...)):
    """Upload and process a PDF document"""
    
    if session_id not in sessions:
        raise HTTPException(404, "Session not found")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files supported")
    
    # Create document metadata
    doc_id = str(uuid.uuid4())
    
    # Store document info
    sessions[session_id]["documents"].append({
        "doc_id": doc_id,
        "filename": file.filename
    })
    
    return {
        "message": f"✅ Document '{file.filename}' uploaded successfully!",
        "doc_id": doc_id,
        "chunks": 42,  # Placeholder
        "session_id": session_id
    }

@app.post("/api/chat/{session_id}")
async def chat(session_id: str, request: ChatRequest):
    """Chat with uploaded documents"""
    
    if session_id not in sessions:
        raise HTTPException(404, "Session not found")
    
    if not sessions[session_id]["documents"]:
        raise HTTPException(400, "No documents uploaded yet")
    
    # Get uploaded document names
    doc_names = [doc["filename"] for doc in sessions[session_id]["documents"]]
    
    return {
        "answer": f"🎉 Your app is working! You've uploaded: {', '.join(doc_names)}. AI document processing will be added in the next version. For now, this confirms your full-stack deployment is successful!",
        "sources": [
            {
                "content": "This is a placeholder response showing the backend is connected.",
                "filename": doc_names[0] if doc_names else "demo.pdf",
                "doc_id": "demo"
            }
        ]
    }