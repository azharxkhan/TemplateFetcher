import React from 'react';
import './App.css';
import TemplateSearch from './TemplateSearch';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>TemplateFetcher</h1>
      </header>

      <main className="app-main">
        <h2>Find the perfect website template</h2>
        <TemplateSearch />
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 TemplateFetcher. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
