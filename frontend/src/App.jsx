import React, { useState } from 'react';
import PaperUpload from './components/PaperUpload';
import QAChat from './components/QAChat';
import './App.css';

export default function App() {
  const [paperFilter, setPaperFilter] = useState('');

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Research Paper Knowledge Base</h1>
        <span className="badge">Production-Grade RAG Architecture v1.0</span>
      </header>

      <main className="app-content">
        <PaperUpload selectedFilter={paperFilter} setSelectedFilter={setPaperFilter} />
        <QAChat paperFilter={paperFilter} />
      </main>
    </div>
  );
}