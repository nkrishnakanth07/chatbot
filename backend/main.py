from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
import tempfile
import os
from openai import OpenAI
from pypdf import PdfReader

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

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        
        if current_size >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

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
        "chunks": [],
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
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Extract text from PDF
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Split into chunks
        chunks = chunk_text(text, chunk_size=1000)
        
        # Create document metadata
        doc_id = str(uuid.uuid4())
        
        # Store chunks with metadata
        for i, chunk in enumerate(chunks):
            sessions[session_id]["chunks"].append({
                "text": chunk,
                "doc_id": doc_id,
                "filename": file.filename,
                "chunk_id": i
            })
        
        # Store document info
        sessions[session_id]["documents"].append({
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks": len(chunks)
        })
        
        return {
            "message": f"✅ Document '{file.filename}' uploaded and processed with AI!",
            "doc_id": doc_id,
            "chunks": len(chunks),
            "session_id": session_id
        }
    
    finally:
        os.unlink(tmp_path)

@app.post("/api/chat/{session_id}")
async def chat(session_id: str, request: ChatRequest):
    """Chat with uploaded documents using AI"""
    
    if session_id not in sessions:
        raise HTTPException(404, "Session not found")
    
    if not sessions[session_id]["chunks"]:
        raise HTTPException(400, "No documents uploaded yet")
    
    try:
        # Initialize OpenAI client here (lazy initialization to avoid startup errors)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Get all document chunks
        all_chunks = sessions[session_id]["chunks"]
        
        # Simple relevance scoring (keyword matching)
        question_lower = request.question.lower()
        scored_chunks = []
        
        for chunk in all_chunks:
            # Count keyword matches
            score = sum(1 for word in question_lower.split() if word in chunk["text"].lower())
            if score > 0:
                scored_chunks.append((score, chunk))
        
        # Sort by score and get top 3
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        relevant_chunks = [chunk for score, chunk in scored_chunks[:3]]
        
        # If no relevant chunks found, use first 3
        if not relevant_chunks:
            relevant_chunks = all_chunks[:3]
        
        # Build context from relevant chunks
        context = "\n\n".join([
            f"From {chunk['filename']} (chunk {chunk['chunk_id']}):\n{chunk['text'][:500]}"
            for chunk in relevant_chunks
        ])
        
        # Build chat history for context
        history_text = ""
        for msg in request.chat_history[-4:]:  # Last 4 messages
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        
        # Create prompt for OpenAI
        prompt = f"""You are a helpful AI assistant answering questions based on uploaded documents.

Previous conversation:
{history_text if history_text else "No previous messages"}

Document context:
{context}

User question: {request.question}

Instructions:
1. Answer the question based ONLY on the provided document context
2. If the answer is in the documents, provide a clear, detailed response
3. If the answer is NOT in the documents, say "I don't see that information in the uploaded documents"
4. Reference the specific document when answering
5. Be concise but thorough

Answer:"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided document context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # Format sources
        sources = []
        for chunk in relevant_chunks:
            sources.append({
                "content": chunk["text"][:200] + "...",
                "filename": chunk["filename"],
                "doc_id": chunk["doc_id"]
            })
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error processing chat: {str(e)}")