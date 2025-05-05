import React, { useState } from 'react';
import axios from 'axios';

function TemplateSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/templates?query=${encodeURIComponent(query)}`);
      setResults(response.data.results);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  return (
    <div>
      <form className="search-form" onSubmit={(e) => { e.preventDefault(); handleSearch(); }}>
        <input
          type="text"
          className="search-input"
          placeholder="e.g. dark portfolio blog"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="search-button">Search</button>
      </form>

      <div className="results-container">
        {results.map((template) => (
          <div key={template.id} className="template-card">
            <h3>{template.title}</h3>
            <img src={template.thumbnail} alt={template.title} width="150" />
            <p>{template.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TemplateSearch;
