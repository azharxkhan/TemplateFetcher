import sqlite3
from fastapi import HTTPException

DATABASE_FILE = "templates.db"

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        thumbnail TEXT,
        url TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_template(title, description, thumbnail, url):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO templates (title, description, thumbnail, url) VALUES (?, ?, ?, ?)",
        (title, description, thumbnail, url),
    )
    conn.commit()
    conn.close()

def get_templates(query: str):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable column names
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM templates WHERE title LIKE ? OR description LIKE ?
    """, (f'%{query}%', f'%{query}%'))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
