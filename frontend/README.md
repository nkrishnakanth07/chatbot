# Multi-Document Chatbot Frontend

A modern React frontend for the multi-document RAG chatbot.

## Features

- ✅ Upload multiple PDF documents
- ✅ Real-time conversation with AI
- ✅ View conversation history
- ✅ Document management (view, delete)
- ✅ Session-based isolation
- ✅ Source citations with document references
- ✅ Beautiful, responsive UI
- ✅ Typing indicators and animations

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update the API URL in `.env` if needed:
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Deployment

### Vercel (Recommended)
1. Push to GitHub
2. Import project to Vercel
3. Add environment variable: `REACT_APP_API_URL=https://your-backend-url.com`
4. Deploy

### Netlify
1. Push to GitHub
2. New site from Git
3. Build command: `npm run build`
4. Publish directory: `build`
5. Add environment variable: `REACT_APP_API_URL=https://your-backend-url.com`

## Usage

1. Upload one or more PDF documents
2. Ask questions about your documents
3. View sources and citations
4. Manage documents (view list, delete)
5. Start new sessions as needed

## Tech Stack

- React 18
- Axios for API calls
- CSS3 with animations
- Responsive design
