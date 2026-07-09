import React, { useState, useEffect } from 'react';

export default function PaperUpload({ selectedFilter, setSelectedFilter }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [papers, setPapers] = useState([]);

  const fetchPapers = async () => {
    try {
      // FORCED IPV4 ADDRESS
      const response = await fetch('http://127.0.0.1:8000/papers');
      if (!response.ok) throw new Error('Failed to retrieve papers.');
      const data = await response.json();
      setPapers(data.papers || []);
    } catch (err) {
      console.error('Error loading papers:', err);
    }
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setMessage('');
      setError('');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file first.');
      return;
    }

    setUploading(true);
    setMessage('Processing and indexing paper...');
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // FORCED IPV4 ADDRESS
      const response = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'An error occurred during upload.');
      }

      setMessage(`Success! Indexed ${data.chunks_indexed} chunks from ${data.filename}`);
      setFile(null);
      document.getElementById('file-upload').value = '';
      await fetchPapers();
    } catch (err) {
      setError(err.message);
      setMessage('');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card text-left">
      <h2>📚 Knowledge Base</h2>
      <p className="subtitle">Upload research papers to add them to your AI's brain.</p>
      
      <form onSubmit={handleUpload} className="upload-container">
        <label htmlFor="file-upload" className={`file-drop-zone ${file ? 'has-file' : ''}`}>
          <div className="drop-icon">{file ? '📄' : '📥'}</div>
          <div className="drop-text">
            {file ? (
              <strong>{file.name}</strong>
            ) : (
              <span><strong>Click to browse</strong> or drag PDF here</span>
            )}
          </div>
        </label>
        <input 
          id="file-upload"
          type="file" 
          accept=".pdf" 
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden-file-input"
        />
        
        <button type="submit" className="btn btn-primary upload-btn" disabled={uploading || !file}>
          {uploading ? 'Indexing...' : 'Add to Knowledge Base'}
        </button>
      </form>

      {message && <div className="status-banner success">{message}</div>}
      {error && <div className="status-banner error">{error}</div>}

      {papers.length > 0 && (
        <div className="filter-section">
          <label htmlFor="paper-filter-dropdown" className="filter-label">🔍 Ask specific paper:</label>
          <select 
            id="paper-filter-dropdown"
            value={selectedFilter} 
            onChange={(e) => setSelectedFilter(e.target.value)}
            className="dropdown"
          >
            <option value="">Query all uploaded documents</option>
            {papers.map((paperName) => (
              <option key={paperName} value={paperName}>
                {paperName}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}