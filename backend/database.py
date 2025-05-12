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

def add_template(title: str, description: str, thumbnail: str, url: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO templates (title, description, thumbnail, url)
    VALUES (?, ?, ?, ?)
    """, (title, description, thumbnail, url))
    conn.commit()
    conn.close()

def get_templates(query: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM templates WHERE title LIKE ? OR description LIKE ?
    """, (f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results
