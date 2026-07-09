import React, { useState, useRef, useEffect } from 'react';

export default function QAChat({ paperFilter }) {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history, loading]);

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');

    const currentQuestion = question;
    setQuestion('');

    try {
      // 1. Safely build the payload so we never send 'null' to strict FastAPI
      const payload = { question: currentQuestion };
      if (paperFilter) {
        payload.paper_filter = paperFilter;
      }

      // 2. Send request to the Python Engine
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      
      // 3. Catch complex FastAPI validation errors safely so they never say [object Object]
      if (!response.ok) {
        const errorMessage = data.detail 
          ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)) 
          : 'Failed to connect to the AI engine.';
        throw new Error(errorMessage);
      }

      const isFallback = data.answer.includes("I could not find this information");

      setHistory((prev) => [
        ...prev,
        {
          question: currentQuestion,
          answer: data.answer,
          sources: data.sources || [],
          isFallback: isFallback,
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card text-left flex-grow">
      <h2>💬 Ask AI Assistant</h2>
      <p className="subtitle">Ask questions based strictly on the facts in your uploaded documents.</p>

      <div className="chat-viewport">
        {history.length === 0 && (
          <div className="empty-chat-state">
            <div className="empty-icon">👋</div>
            <h3>How can I help you today?</h3>
            <p>Upload a paper above and ask me anything about it.</p>
          </div>
        )}
        
        {history.map((turn, idx) => (
          <div key={idx} className="chat-exchange">
            <div className="chat-bubble user-query">
              {turn.question}
            </div>
            
            <div className={`chat-bubble bot-response ${turn.isFallback ? 'fallback-style' : ''}`}>
              <div className="bot-answer-text">{turn.answer}</div>
              
              {turn.sources.length > 0 && (
                <div className="citation-tray">
                  <h4>Sources cited:</h4>
                  <ul>
                    {turn.sources.map((src, i) => (
                      <li key={i}>📄 {src}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-exchange">
            <div className="chat-bubble bot-response loading-bubble">
              <div className="spinner"></div>
              <span>Reading papers...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {error && <div className="status-banner error">{error}</div>}

      <form onSubmit={handleAskQuestion} className="chat-input-form">
        <input
          type="text"
          placeholder={paperFilter ? `Asking about ${paperFilter}...` : "Ask a question..."}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
          className="chat-input-box"
        />
        <button type="submit" className="btn btn-secondary send-btn" disabled={loading || !question.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}