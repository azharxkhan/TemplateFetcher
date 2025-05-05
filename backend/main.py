from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Allow frontend requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/templates")
def get_templates(query: str = Query(..., min_length=1)):
    # Mock data for now — later this will call your scraper
    mock_templates = [
        {"id": 1, "title": "Dark Portfolio", "thumbnail": "https://via.placeholder.com/150", "description": "A sleek dark-themed portfolio template."},
        {"id": 2, "title": "Minimal Blog", "thumbnail": "https://via.placeholder.com/150", "description": "A minimalistic blog theme."},
    ]
    # Filter mock results based on query string
    filtered = [t for t in mock_templates if query.lower() in t["title"].lower()]
    return {"results": filtered}
