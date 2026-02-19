import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

// Use relative URLs for Vercel deployment, fallback to localhost for development
const API_URL = process.env.NODE_ENV === 'production' ? '' : (process.env.REACT_APP_API_URL || 'http://localhost:8000');

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [showDocuments, setShowDocuments] = useState(false);
  const messagesEndRef = useRef(null);

  // Create session on mount
  useEffect(() => {
    createSession();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const createSession = async () => {
    try {
      const res = await axios.post(`${API_URL}/api/session/create`);
      setSessionId(res.data.session_id);
      setMessages([{
        role: 'assistant',
        content: 'Hello! Upload one or more PDF documents to start chatting. I can answer questions across all your uploaded documents.',
        timestamp: new Date().toISOString()
      }]);
    } catch (err) {
      console.error('Failed to create session:', err);
      alert('Failed to create session. Please refresh the page.');
    }
  };

  const uploadDocument = async (file) => {
    if (!sessionId) {
      alert('Session not ready. Please wait...');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/api/upload/${sessionId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      const newDoc = {
        doc_id: res.data.doc_id,
        filename: file.name,
        chunks: res.data.chunks
      };
      
      setDocuments(prev => [...prev, newDoc]);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `✅ Document "${file.name}" uploaded! (${res.data.chunks} chunks processed). You can now ask questions about your documents.`,
        timestamp: new Date().toISOString()
      }]);
    } catch (err) {
      console.error('Upload failed:', err);
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    }
    setLoading(false);
  };

  const sendMessage = async () => {
    if (!input.trim() || !sessionId) return;
    
    const userMsg = { 
      role: 'user', 
      content: input,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    
    try {
      const res = await axios.post(`${API_URL}/api/chat/${sessionId}`, {
        session_id: sessionId,
        question: input,
        chat_history: messages
      });
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources,
        timestamp: new Date().toISOString()
      }]);
    } catch (err) {
      console.error('Chat failed:', err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Error: ' + (err.response?.data?.detail || err.message),
        timestamp: new Date().toISOString()
      }]);
    }
    setLoading(false);
  };

  const startNewSession = () => {
    if (window.confirm('Start a new session? This will clear your current conversation and documents.')) {
      setMessages([]);
      setDocuments([]);
      createSession();
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>📄 Multi-Document Chat Assistant</h1>
          <div className="header-actions">
            <button 
              className="btn-secondary" 
              onClick={() => setShowDocuments(!showDocuments)}
            >
              📚 Documents ({documents.length})
            </button>
            <button 
              className="btn-secondary" 
              onClick={startNewSession}
            >
              🔄 New Session
            </button>
          </div>
        </header>

        {showDocuments && (
          <div className="documents-panel">
            <h3>Uploaded Documents</h3>
            {documents.length === 0 ? (
              <p className="empty-state">No documents uploaded yet</p>
            ) : (
              <div className="documents-list">
                {documents.map(doc => (
                  <div key={doc.doc_id} className="document-item">
                    <div className="doc-info">
                      <span className="doc-name">📄 {doc.filename}</span>
                      <span className="doc-chunks">{doc.chunks} chunks</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="upload-zone">
          <input
            type="file"
            id="file-upload"
            accept=".pdf"
            onChange={(e) => e.target.files[0] && uploadDocument(e.target.files[0])}
            disabled={loading || !sessionId}
            style={{ display: 'none' }}
          />
          <label htmlFor="file-upload" className={`upload-label ${loading ? 'disabled' : ''}`}>
            📎 Upload PDF Document
          </label>
          {documents.length === 0 && (
            <p className="upload-hint">Upload one or more PDFs to get started</p>
          )}
        </div>
        
        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="message-header">
                <span className="message-role">
                  {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
                </span>
                {msg.timestamp && (
                  <span className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                )}
              </div>
              <div className="content">{msg.content}</div>
              {msg.sources && msg.sources.length > 0 && (
                <details className="sources">
                  <summary>📚 View {msg.sources.length} source(s)</summary>
                  {msg.sources.map((src, j) => (
                    <div key={j} className="source">
                      <div className="source-filename">From: {src.filename}</div>
                      <div className="source-content">{src.content}...</div>
                    </div>
                  ))}
                </details>
              )}
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-header">
                <span className="message-role">🤖 Assistant</span>
              </div>
              <div className="content typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        {documents.length > 0 && (
          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder="Ask a question about your documents..."
              disabled={loading}
            />
            <button 
              onClick={sendMessage} 
              disabled={loading || !input.trim()}
              className="btn-send"
            >
              {loading ? '⏳' : '📤'} Send
            </button>
          </div>
        )}

        <div className="footer">
          <p>Session ID: {sessionId ? sessionId.slice(0, 8) + '...' : 'Loading...'}</p>
          <p>Powered by OpenAI GPT-4 • {messages.filter(m => m.role === 'user').length} questions asked</p>
        </div>
      </div>
    </div>
  );
}

export default App;
