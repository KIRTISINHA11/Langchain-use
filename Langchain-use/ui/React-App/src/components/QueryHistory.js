import React from 'react';
import './QueryHistory.css';

function QueryHistory({ history }) {
  const questions = history.filter(msg => msg.type === 'user');

  return (
    <div className="query-history-panel">
      <h3>📋 Query History</h3>
      <div className="history-list">
        {questions.length === 0 ? (
          <p className="empty-history">No queries yet</p>
        ) : (
          questions.map((q, idx) => (
            <div key={idx} className="history-item" title={q.content}>
              <span className="history-index">{idx + 1}.</span>
              <span className="history-text">{q.content.substring(0, 40)}...</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default QueryHistory;
