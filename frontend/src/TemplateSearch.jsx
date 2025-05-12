import React, { useState } from 'react';
import axios from 'axios';
import './TemplateSearch.css'; 

function TemplateSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a search term.");
      return;
    }

    setLoading(true);
    setError(null);
    setResults([]);
    
    try {
      const response = await axios.get(`http://localhost:8000/templates?query=${encodeURIComponent(query)}`);
      setResults(response.data.results || []);
    } catch (err) {
      setError("Failed to fetch templates. Please try again later.");
      console.error("Error fetching templates:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="template-search-container">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search templates..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">Search</button>
      </div>

      {loading && <p className="loading-text">Loading...</p>}
      {error && <p className="error-text">{error}</p>}

      <div className="results-container">
        {results.length > 0 ? (
          results.map((template, index) => (
            <div key={index} className="template-card">
              <img src={template.thumbnail} alt={template.title} className="template-image" />
              <h3>{template.title}</h3>
              <p>{template.description}</p>
            </div>
          ))
        ) : (
          !loading && <p className="no-results-text">No templates found.</p>
        )}
      </div>
    </div>
  );
}

export default TemplateSearch;
