from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from mangum import Mangum
import json
import tempfile
from typing import List, Optional
import uuid
from datetime import datetime

# Import LangChain components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from pypdf import PdfReader

# For serverless, we'll use Pinecone instead of ChromaDB
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

app = FastAPI(title="Multi-Document RAG Chatbot - Vercel")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone (better for serverless than ChromaDB)
def get_pinecone_index():
    """Initialize Pinecone index"""
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    index_name = "chatbot-docs"
    
    # Create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI embedding dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    return pc.Index(index_name)

# Initialize OpenAI
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

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
    return SessionResponse(
        session_id=session_id,
        message="Session created successfully"
    )

@app.post("/api/upload/{session_id}")
async def upload_document(session_id: str, file: UploadFile = File(...)):
    """Upload and process a PDF document"""
    
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
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_text(text)
        
        # Create document metadata
        doc_id = str(uuid.uuid4())
        
        # Create metadata for each chunk
        metadatas = [
            {
                "doc_id": doc_id,
                "filename": file.filename,
                "chunk_id": i,
                "session_id": session_id
            } 
            for i in range(len(chunks))
        ]
        
        # Store in Pinecone
        index = get_pinecone_index()
        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
            text_key="text"
        )
        
        vectorstore.add_texts(
            texts=chunks,
            metadatas=metadatas
        )
        
        return {
            "message": f"Document '{file.filename}' uploaded and processed",
            "doc_id": doc_id,
            "chunks": len(chunks),
            "session_id": session_id
        }
    
    finally:
        os.unlink(tmp_path)

@app.post("/api/chat/{session_id}")
async def chat(session_id: str, request: ChatRequest):
    """Chat with uploaded documents"""
    
    try:
        # Get Pinecone vectorstore
        index = get_pinecone_index()
        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
            text_key="text"
        )
        
        # Create retriever with session filter
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 4,
                "filter": {"session_id": session_id}
            }
        )
        
        # Create QA chain
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        
        # Format chat history for LangChain
        chat_history = []
        for msg in request.chat_history:
            if msg["role"] == "user":
                chat_history.append((msg["content"], ""))
            elif msg["role"] == "assistant" and chat_history:
                chat_history[-1] = (chat_history[-1][0], msg["content"])
        
        # Get response
        result = qa_chain({
            "question": request.question,
            "chat_history": chat_history
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
            "sources": sources
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error processing chat: {str(e)}")

# Vercel serverless handler
handler = Mangum(app, lifespan="off")
