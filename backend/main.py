from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from pypdf import PdfReader
import tempfile
import uuid
from typing import List, Optional
import json
from datetime import datetime

load_dotenv()

app = FastAPI(title="Multi-Document RAG Chatbot")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for sessions and documents
sessions = {}
documents_db = {}

# Initialize OpenAI components
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    session_id: str
    question: str

class SessionResponse(BaseModel):
    session_id: str
    message: str

class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    chunks: int
    upload_time: str

def create_session(session_id: Optional[str] = None) -> str:
    """Create a new chat session"""
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = {
            "vectorstore": None,
            "qa_chain": None,
            "chat_history": [],
            "documents": [],
            "created_at": datetime.now().isoformat()
        }
    
    return session_id

def get_session(session_id: str):
    """Get session or create if not exists"""
    if session_id not in sessions:
        create_session(session_id)
    return sessions[session_id]

@app.post("/session/create", response_model=SessionResponse)
async def create_new_session():
    """Create a new chat session"""
    session_id = create_session()
    return SessionResponse(
        session_id=session_id,
        message="Session created successfully"
    )

@app.post("/upload/{session_id}")
async def upload_document(session_id: str, file: UploadFile = File(...)):
    """Upload and process a PDF document to a specific session"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files supported")
    
    session = get_session(session_id)
    
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
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_text(text)
        
        # Create document metadata
        doc_id = str(uuid.uuid4())
        metadatas = [{"doc_id": doc_id, "filename": file.filename, "chunk_id": i} 
                     for i in range(len(chunks))]
        
        # Add to existing vectorstore or create new one
        if session["vectorstore"] is None:
            session["vectorstore"] = Chroma.from_texts(
                texts=chunks,
                embedding=embeddings,
                metadatas=metadatas,
                persist_directory=f"./chroma_db/{session_id}"
            )
        else:
            session["vectorstore"].add_texts(
                texts=chunks,
                metadatas=metadatas
            )
        
        # Update or create QA chain
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        session["qa_chain"] = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=session["vectorstore"].as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            verbose=True
        )
        
        # Store document info
        doc_info = {
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks": len(chunks),
            "upload_time": datetime.now().isoformat()
        }
        session["documents"].append(doc_info)
        documents_db[doc_id] = doc_info
        
        return {
            "message": f"Document '{file.filename}' uploaded and processed",
            "doc_id": doc_id,
            "chunks": len(chunks),
            "total_documents": len(session["documents"])
        }
    
    finally:
        os.unlink(tmp_path)

@app.post("/chat/{session_id}")
async def chat(session_id: str, request: ChatRequest):
    """Chat with the uploaded documents in a session"""
    session = get_session(session_id)
    
    if not session["qa_chain"]:
        raise HTTPException(400, "No documents uploaded in this session yet")
    
    # Convert chat history to LangChain format
    chat_history = []
    for msg in session["chat_history"]:
        if msg["role"] == "user":
            chat_history.append((msg["content"], ""))
        elif msg["role"] == "assistant" and chat_history:
            chat_history[-1] = (chat_history[-1][0], msg["content"])
    
    # Get response from chain
    result = session["qa_chain"]({
        "question": request.question,
        "chat_history": chat_history
    })
    
    # Store in session history
    session["chat_history"].append({
        "role": "user",
        "content": request.question,
        "timestamp": datetime.now().isoformat()
    })
    session["chat_history"].append({
        "role": "assistant",
        "content": result["answer"],
        "timestamp": datetime.now().isoformat()
    })
    
    # Extract source information
    sources = []
    for doc in result.get("source_documents", []):
        sources.append({
            "content": doc.page_content[:200],
            "filename": doc.metadata.get("filename", "Unknown"),
            "doc_id": doc.metadata.get("doc_id", "Unknown")
        })
    
    return {
        "answer": result["answer"],
        "sources": sources,
        "chat_history_length": len(session["chat_history"])
    }

@app.get("/session/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    session = get_session(session_id)
    return {
        "session_id": session_id,
        "chat_history": session["chat_history"],
        "documents": session["documents"]
    }

@app.get("/session/{session_id}/documents")
async def get_session_documents(session_id: str):
    """Get all documents in a session"""
    session = get_session(session_id)
    return {
        "session_id": session_id,
        "documents": session["documents"],
        "total": len(session["documents"])
    }

@app.delete("/session/{session_id}/document/{doc_id}")
async def delete_document(session_id: str, doc_id: str):
    """Delete a document from session (note: doesn't remove from vectorstore in this implementation)"""
    session = get_session(session_id)
    session["documents"] = [d for d in session["documents"] if d["doc_id"] != doc_id]
    return {"message": "Document removed from session", "remaining": len(session["documents"])}

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and its data"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session deleted"}
    raise HTTPException(404, "Session not found")

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "active_sessions": len(sessions),
        "total_documents": sum(len(s["documents"]) for s in sessions.values())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
