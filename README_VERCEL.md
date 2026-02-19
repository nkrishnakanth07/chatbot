# 📄 Multi-Document RAG Chatbot - Vercel Edition

A full-stack serverless chatbot that lets you upload multiple PDFs and ask questions across all of them. Deployed entirely on Vercel's free tier!

## 🌟 Live Demo

**[Try it here!](https://your-app.vercel.app)** ← (Replace with your Vercel URL after deployment)

## ✨ Features

- 📄 **Upload multiple PDFs** - Add as many documents as you need
- 💬 **Ask questions across all documents** - The AI searches all your uploaded files
- 📚 **Source citations** - See exactly where answers came from
- 🚀 **100% Serverless** - Deployed on Vercel's free tier
- 🔒 **Session-based** - Your conversations are isolated
- ⚡ **Fast responses** - Powered by OpenAI GPT-4o-mini
- 🌍 **Global CDN** - Fast loading worldwide

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Axios for API calls
- Modern CSS with animations

**Backend:**
- FastAPI (Vercel Serverless Functions)
- LangChain for RAG pipeline
- OpenAI GPT-4o-mini
- Pinecone vector database
- Mangum for AWS Lambda/Vercel adapter

**Deployment:**
- Vercel (Frontend + Serverless Backend)
- Free tier only! $0/month infrastructure

## 🚀 Quick Deploy to Vercel

### Prerequisites
1. GitHub account
2. Vercel account (sign up with GitHub)
3. OpenAI API key ([get one here](https://platform.openai.com/api-keys))
4. Pinecone account ([sign up free](https://www.pinecone.io))

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/chatbot-vercel)

**OR follow the detailed guide:** [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)

### Quick Steps:

1. **Get API Keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Pinecone: https://www.pinecone.io → API Keys

2. **Fork & Deploy:**
   ```bash
   # Clone this repo
   git clone https://github.com/YOUR_USERNAME/chatbot-vercel
   cd chatbot-vercel
   
   # Push to your GitHub
   git remote set-url origin https://github.com/YOUR_USERNAME/your-repo
   git push
   ```

3. **Deploy on Vercel:**
   - Go to https://vercel.com/new
   - Import your repository
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `PINECONE_API_KEY`
     - `PINECONE_ENVIRONMENT`
   - Click Deploy!

4. **Done!** Your app is live in 3-5 minutes 🎉

## 💻 Local Development

### Backend + Frontend Together

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Run Vercel dev server (runs both frontend and backend)
vercel dev
```

Visit http://localhost:3000

### Separate Development (Optional)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm start
```

## 📁 Project Structure

```
chatbot-vercel/
├── api/
│   └── index.py              # Vercel serverless function (FastAPI)
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   └── App.css          # Styles
│   ├── public/
│   └── package.json
├── backend/                  # Local development backend (optional)
│   └── main.py              # Original FastAPI app
├── requirements.txt          # Python dependencies for Vercel
├── vercel.json              # Vercel configuration
├── VERCEL_DEPLOY.md         # Detailed deployment guide
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Set these in Vercel dashboard or `.env` for local dev:

```bash
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk-...
PINECONE_ENVIRONMENT=us-east-1
```

### Customization

**Change AI Model:**
```python
# In api/index.py
llm = ChatOpenAI(
    model="gpt-4o",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0
)
```

**Adjust Chunk Size:**
```python
# In api/index.py
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Larger = more context
    chunk_overlap=300
)
```

**Change Retrieved Chunks:**
```python
# In api/index.py
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 6}  # Retrieve more chunks
)
```

## 💰 Costs

### Free Tier
- **Vercel:** Free forever for personal projects
- **Pinecone:** 1 free serverless index (100K vectors)
- **OpenAI:** Pay per use (~$1-5/month for light testing)

### Scaling
- **Light Use** (portfolio/demo): $0-5/month
- **Moderate Use** (50-100 queries/day): $5-20/month
- **Heavy Use:** Upgrade Pinecone ($70/month) + OpenAI usage

## 🎯 Use Cases

- 📚 Research assistant for academic papers
- 📄 Corporate document Q&A
- 📖 Book/manual chatbot
- 🏢 Internal knowledge base
- 📝 Legal document analysis
- 🎓 Study assistant for textbooks

## 🔒 Security

- ✅ HTTPS by default (Vercel)
- ✅ Environment variables for secrets
- ✅ Session-based isolation
- ✅ No data persistence (serverless)
- ⚠️ Add authentication for production use

## 📊 Performance

- **Cold Start:** 2-5 seconds (first request)
- **Warm Responses:** 500ms - 2s
- **File Upload:** ~5-10s for typical PDF
- **Global CDN:** Fast loading worldwide

## 🐛 Troubleshooting

**Build Fails:**
- Check Vercel build logs
- Verify all dependencies in requirements.txt
- Ensure vercel.json is correct

**API Errors:**
- Check Vercel function logs
- Verify environment variables are set
- Check OpenAI and Pinecone API keys

**Slow Responses:**
- Pinecone free tier has rate limits
- Reduce chunk count (k=2 instead of k=4)
- Use GPT-4o-mini instead of GPT-4

## 🤝 Contributing

This is a portfolio/learning project, but PRs are welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

## 📝 License

MIT License - feel free to use for your portfolio!

## 🙏 Acknowledgments

Built with:
- [LangChain](https://python.langchain.com)
- [OpenAI](https://openai.com)
- [Pinecone](https://www.pinecone.io)
- [Vercel](https://vercel.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [React](https://react.dev)

## 📧 Contact

Questions? Issues? Improvements?
- Open an issue on GitHub
- Check [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md) for detailed help

---

**⭐ Star this repo if you found it helpful!**

Built with ❤️ and deployed on Vercel's free tier 🚀
