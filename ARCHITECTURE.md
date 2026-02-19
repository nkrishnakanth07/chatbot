# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                      (React Frontend)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Session Manager                         │   │
│  │  • Create/Delete Sessions                           │   │
│  │  • Store Conversation History                       │   │
│  │  • Manage Document Metadata                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │           Document Processing                         │ │
│  │  • PDF Text Extraction (PyPDF)                       │ │
│  │  • Text Chunking (RecursiveCharacterTextSplitter)    │ │
│  │  • Metadata Addition                                 │ │
│  └─────────────────────────┬─────────────────────────────┘ │
│                            │                                 │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │           Vector Store (ChromaDB)                     │ │
│  │  • Store Document Embeddings                         │ │
│  │  • Semantic Search                                   │ │
│  │  • Multi-Document Indexing                           │ │
│  └─────────────────────────┬─────────────────────────────┘ │
│                            │                                 │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │        LangChain RAG Pipeline                         │ │
│  │  • ConversationalRetrievalChain                      │ │
│  │  • Context Window Management                         │ │
│  │  • Source Document Retrieval                         │ │
│  └─────────────────────────┬─────────────────────────────┘ │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             │ API Calls
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                     OpenAI GPT-4 API                          │
│  • Generate Responses                                         │
│  • Create Embeddings                                          │
│  • Maintain Conversation Context                             │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Upload Flow

```
User Upload PDF
     │
     ▼
Frontend (React)
     │ FormData
     ▼
Backend (/upload/{session_id})
     │
     ├──► PyPDF: Extract Text
     │
     ├──► Text Splitter: Create Chunks
     │         │
     │         └──► Chunks (1000 chars, 200 overlap)
     │
     ├──► OpenAI: Generate Embeddings
     │
     └──► ChromaDB: Store Vectors + Metadata
           │
           └──► Return: {doc_id, chunks, status}
```

### 2. Chat Query Flow

```
User Question
     │
     ▼
Frontend (React)
     │ {session_id, question, chat_history}
     ▼
Backend (/chat/{session_id})
     │
     ├──► ChromaDB: Semantic Search (k=4)
     │         │
     │         └──► Relevant Chunks + Metadata
     │
     ├──► LangChain: Build Context
     │         │
     │         ├──► Question
     │         ├──► Retrieved Chunks
     │         └──► Chat History
     │
     ├──► OpenAI GPT-4: Generate Answer
     │         │
     │         └──► Response + Reasoning
     │
     └──► Store History + Return
           │
           └──► {answer, sources, metadata}
```

## Components Breakdown

### Frontend (React)

**Components:**
- `App.js` - Main application component
  - State management (sessions, messages, documents)
  - API communication
  - UI rendering

**Key Features:**
- Session initialization on mount
- File upload handling
- Real-time message streaming
- Document list management
- Source citation display

**State Structure:**
```javascript
{
  sessionId: "uuid",
  messages: [
    {role: "user", content: "...", timestamp: "..."},
    {role: "assistant", content: "...", sources: [...]}
  ],
  documents: [
    {doc_id: "...", filename: "...", chunks: 123}
  ],
  loading: false
}
```

### Backend (FastAPI)

**Core Modules:**

1. **Session Management**
   - In-memory storage (sessions dict)
   - Session creation/deletion
   - Document tracking per session

2. **Document Processing**
   - PDF text extraction
   - Chunking with overlap
   - Metadata tagging

3. **Vector Store (ChromaDB)**
   - Persistent storage per session
   - Incremental document addition
   - Semantic search

4. **LangChain Integration**
   - ConversationalRetrievalChain
   - History management
   - Source document tracking

**Session Structure:**
```python
{
  "session_id": {
    "vectorstore": ChromaDB,
    "qa_chain": ConversationalRetrievalChain,
    "chat_history": [{role, content, timestamp}],
    "documents": [{doc_id, filename, chunks}],
    "created_at": "ISO timestamp"
  }
}
```

## Key Technologies

### Vector Embeddings
- **Model**: OpenAI text-embedding-ada-002
- **Dimensions**: 1536
- **Use**: Convert text to semantic vectors for similarity search

### Text Chunking Strategy
- **Size**: 1000 characters per chunk
- **Overlap**: 200 characters
- **Reason**: Balances context vs. specificity

### RAG Pipeline
1. **Retrieve**: Find top-k relevant chunks (k=4)
2. **Augment**: Add chunks to prompt context
3. **Generate**: LLM produces answer with sources

## Scalability Considerations

### Current Limitations (Free Tier)
- In-memory session storage (lost on restart)
- Single server instance
- No load balancing
- ~50 concurrent users max

### Production Improvements

**1. Database Integration**
```
PostgreSQL for:
- User accounts
- Session persistence
- Document metadata
- Conversation history
```

**2. Vector Store**
```
Pinecone/Weaviate for:
- Distributed vector storage
- Faster search
- Better scalability
```

**3. Caching Layer**
```
Redis for:
- Session caching
- Query result caching
- Rate limiting
```

**4. Queue System**
```
Celery + RabbitMQ for:
- Async document processing
- Background tasks
- Job scheduling
```

## Security Layers

### Current Implementation
- CORS enabled (all origins in dev)
- No authentication
- Rate limiting: None
- Input validation: File type only

### Production Recommendations

**1. Authentication**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    # Verify JWT token
    pass
```

**2. Rate Limiting**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(...):
    pass
```

**3. Input Sanitization**
```python
from bleach import clean

def sanitize_input(text: str) -> str:
    return clean(text, strip=True)
```

**4. File Validation**
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["application/pdf"]

def validate_file(file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")
```

## Performance Optimization

### Backend
- **Caching**: Cache embeddings for repeated uploads
- **Batching**: Process multiple documents in parallel
- **Streaming**: Stream LLM responses to reduce latency
- **Connection Pooling**: Reuse HTTP connections to OpenAI

### Frontend
- **Lazy Loading**: Load messages on scroll
- **Debouncing**: Delay search queries
- **Memoization**: Cache rendered components
- **Code Splitting**: Load code on demand

## Monitoring & Observability

### Metrics to Track
- API response times
- OpenAI token usage
- Error rates
- Active sessions
- Document upload success rate

### Logging Strategy
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.post("/chat")
async def chat(...):
    logger.info(f"Chat request - Session: {session_id}")
    # ... handle request
    logger.info(f"Response time: {elapsed}ms")
```

## Cost Analysis

### OpenAI API Costs (GPT-4o-mini)

**Embeddings** (text-embedding-ada-002):
- $0.0001 per 1K tokens
- ~1 page PDF = ~500 tokens
- 100 pages = $0.05

**Generation** (GPT-4o-mini):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- Average query: ~2K input + 500 output = $0.0006

**Monthly Estimate** (100 users, 10 queries/day):
- Embeddings: ~$15/month
- Generation: ~$18/month
- **Total: ~$33/month**

### Infrastructure Costs

**Free Tier:**
- Render: $0
- Vercel: $0
- Total: **$0/month**

**Paid Tier (recommended for production):**
- Render Starter: $7/month
- Vercel Pro: $20/month
- Database: $5-10/month
- Total: **$32-37/month**

## Future Enhancements

### Phase 1 (MVP+)
- [ ] User authentication
- [ ] Persistent database
- [ ] Rate limiting
- [ ] Usage analytics

### Phase 2 (Scale)
- [ ] Support more file types
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Export conversations

### Phase 3 (Advanced)
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Collaborative sessions
- [ ] Custom model fine-tuning

---

This architecture is designed to be simple for learning/portfolio but extensible for production use!
