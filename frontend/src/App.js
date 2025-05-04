import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>TemplateFetcher</h1>
      </header>

      <main className="app-main">
        <h2>Find the perfect website template</h2>
        <form className="search-form" onSubmit={(e) => e.preventDefault()}>
          <input
            type="text"
            className="search-input"
            placeholder="e.g. dark portfolio blog"
          />
          <button type="submit" className="search-button">Search</button>
        </form>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 TemplateFetcher. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
