from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

router = APIRouter()

# Temporary in-memory storage for templates
TEMPLATES = [
    {
        "id": 1,
        "title": "Dark Portfolio Blog",
        "description": "A modern dark-themed portfolio template.",
        "thumbnail": "https://via.placeholder.com/150",
        "url": "https://example.com/template1"
    },
    {
        "id": 2,
        "title": "Bright Business Landing",
        "description": "A clean and minimal landing page for businesses.",
        "thumbnail": "https://via.placeholder.com/150",
        "url": "https://example.com/template2"
    }
]

@router.get("/templates")
def search_templates(query: Optional[str] = Query(None)):
    if not query:
        return {"results": TEMPLATES}
    
    filtered_templates = [
        template for template in TEMPLATES 
        if query.lower() in template["title"].lower()
        or query.lower() in template["description"].lower()
    ]
    
    if not filtered_templates:
        raise HTTPException(status_code=404, detail="No templates found.")
    
    return {"results": filtered_templates}
