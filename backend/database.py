import sqlite3
from typing import List, Dict
import asyncio

from backend.util.scraping.colorlib_scraper import scrape_colorlib
from backend.util.scraping.playwright_scraper import scrape_wix

DATABASE_FILE = "templates.db"

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                thumbnail TEXT,
                url TEXT
            )
        """)
        conn.commit()

def add_template(title: str, description: str, thumbnail: str, url: str) -> None:
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO templates VALUES (NULL, ?, ?, ?, ?)",
            (title, description, thumbnail, url)
        )
        conn.commit()

def get_templates(query: str) -> List[Dict]:
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM templates 
            WHERE title LIKE ? OR description LIKE ?
        """, (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]

async def scrape_templates(query: str = ""):
    print("Scraping templates...")
    try:
        wix_templates = await scrape_wix()
        colorlib_templates = await scrape_colorlib(query)
        all_templates = wix_templates + colorlib_templates
        
        for template in all_templates:
            add_template(
                template["title"],
                template["title"],  # Using title as description temporarily
                template["image_url"],
                template["link"]
            )
        
        print(f"✅ Added {len(all_templates)} templates to the database.")
        return all_templates
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
