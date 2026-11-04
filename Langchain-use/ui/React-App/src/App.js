import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import QueryHistory from './components/QueryHistory';
import { FiMenu, FiX } from 'react-icons/fi';

function App() {
  const [documents, setDocuments] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [apiStatus, setApiStatus] = useState('checking');
  const chatEndRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    checkApiStatus();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 3000 });
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
      console.error('API connection failed:', error);
    }
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      });

      setDocuments([...documents, response.data]);
      setChatHistory([
        ...chatHistory,
        {
          type: 'system',
          content: `✅ Document "${file.name}" uploaded and processed successfully!`,
          timestamp: new Date(),
        },
      ]);
    } catch (error) {
      setChatHistory([
        ...chatHistory,
        {
          type: 'error',
          content: `❌ Failed to upload: ${error.response?.data?.detail || error.message}`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (question) => {
    if (!documents.length) {
      setChatHistory([
        ...chatHistory,
        { type: 'user', content: question, timestamp: new Date() },
        {
          type: 'error',
          content: '⚠️ Please upload a document first!',
          timestamp: new Date(),
        },
      ]);
      return;
    }

    setChatHistory([...chatHistory, { type: 'user', content: question, timestamp: new Date() }]);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        question,
      }, {
        timeout: 60000,
      });

      setChatHistory((prev) => [
        ...prev,
        {
          type: 'assistant',
          content: response.data.answer,
          sources: response.data.sources,
          confidence: response.data.confidence,
          timestamp: new Date(),
        },
      ]);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        {
          type: 'error',
          content: `❌ Error: ${error.response?.data?.detail || error.message}`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    setChatHistory([]);
    setDocuments([]);
  };

  return (
    <div className="app-container">
      <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h1>🔍 ZSearch</h1>
          <button
            className="sidebar-toggle mobile-only"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>

        <div className="api-status">
          <div className={`status-indicator ${apiStatus}`}></div>
          <span>{apiStatus === 'connected' ? '🟢 Connected' : '🔴 Disconnected'}</span>
        </div>

        <FileUpload onFileUpload={handleFileUpload} loading={loading} />

        <div className="sidebar-footer">
          {documents.length > 0 && (
            <div className="documents-info">
              <h3>📄 Loaded Documents</h3>
              <ul>
                {documents.map((doc, idx) => (
                  <li key={idx}>{doc.filename || `Document ${idx + 1}`}</li>
                ))}
              </ul>
            </div>
          )}

          <button className="clear-btn" onClick={clearHistory} disabled={chatHistory.length === 0}>
            Clear History
          </button>
        </div>
      </div>

      <div className="main-content">
        <div className="chat-container">
          <ChatInterface
            chatHistory={chatHistory}
            onQuery={handleQuery}
            loading={loading}
            apiStatus={apiStatus}
            ref={chatEndRef}
          />
        </div>

        <div className={`query-history ${sidebarOpen ? 'hidden' : 'visible'}`}>
          <QueryHistory history={chatHistory} />
        </div>
      </div>
    </div>
  );
}

export default App;
