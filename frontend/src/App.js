import React from 'react';
import './App.css';
import TemplateSearch from './TemplateSearch'; // ⬅️ Import your component

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>TemplateFetcher</h1>
      </header>

      <main className="app-main">
        <h2>Find the perfect website template</h2>
        <TemplateSearch /> {/* ⬅️ Use the component here */}
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 TemplateFetcher. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
