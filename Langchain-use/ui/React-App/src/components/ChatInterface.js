import React, { useState, useEffect, forwardRef } from 'react';
import { FiSend } from 'react-icons/fi';
import './ChatInterface.css';

const ChatInterface = forwardRef(({ chatHistory, onQuery, loading, apiStatus }, ref) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading && apiStatus === 'connected') {
      onQuery(input);
      setInput('');
    }
  };

  useEffect(() => {
    const chatArea = document.querySelector('.chat-messages');
    if (chatArea) {
      chatArea.scrollTop = chatArea.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 Chat</h2>
        <p className="chat-subtitle">Ask questions about your documents</p>
      </div>

      <div className="chat-messages">
        {chatHistory.length === 0 ? (
          <div className="chat-empty">
            <div className="empty-icon">🚀</div>
            <p>Welcome to ZSearch!</p>
            <p className="empty-text">
              Upload a document and start asking questions to get instant answers powered by RAG.
            </p>
          </div>
        ) : (
          chatHistory.map((message, idx) => (
            <div
              key={idx}
              className={`chat-message ${message.type}`}
            >
              <div className="message-avatar">
                {message.type === 'user' && '👤'}
                {message.type === 'assistant' && '🤖'}
                {message.type === 'system' && '✅'}
                {message.type === 'error' && '❌'}
              </div>
              <div className="message-content">
                <p className="message-text">{message.content}</p>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <p className="sources-title">📚 Sources:</p>
                    <ul>
                      {message.sources.map((source, i) => (
                        <li key={i}>
                          <strong>{source.document}</strong>
                          {source.page && ` - Page ${source.page}`}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {message.confidence && (
                  <div className="message-confidence">
                    🎯 Confidence: {(message.confidence * 100).toFixed(1)}%
                  </div>
                )}
                <span className="message-time">
                  {new Date(message.timestamp).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </div>
            </div>
          ))
        )}
        <div ref={ref} />
      </div>

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder={
            apiStatus === 'disconnected'
              ? '🔴 API disconnected...'
              : 'Ask a question about your document...'
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading || apiStatus === 'disconnected'}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!input.trim() || loading || apiStatus === 'disconnected'}
        >
          {loading ? (
            <span className="loader">⏳</span>
          ) : (
            <FiSend size={20} />
          )}
        </button>
      </form>
    </div>
  );
});

ChatInterface.displayName = 'ChatInterface';

export default ChatInterface;
