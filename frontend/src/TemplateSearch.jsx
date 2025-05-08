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
      <input
        type="text"
        placeholder="Search templates..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input"
      />
      <button onClick={handleSearch} className="search-button">Search</button>

      <div className="results-container">
        {results.map((template) => (
          <div key={template.id} className="template-card">
            <img src={template.thumbnail} alt={template.title} />
            <h3>{template.title}</h3>
            <p>{template.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TemplateSearch;
