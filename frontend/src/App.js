import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/search?q=${query}`);
      setTemplates(response.data.templates);
    } catch (err) {
      console.error("Error fetching templates:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>TemplateFetcher</h1>
      <input
        type="text"
        placeholder="Search for a template (e.g. dark blog)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={fetchTemplates} disabled={loading}>
        {loading ? "Loading..." : "Search"}
      </button>

      <div className="results">
        {templates.length > 0 ? (
          templates.map((template, index) => (
            <div key={index} className="template-card">
              <h3>{template.title}</h3>
              <a href={template.url} target="_blank" rel="noopener noreferrer">
                View Template
              </a>
            </div>
          ))
        ) : (
          <p>No templates found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
