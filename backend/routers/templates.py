from fastapi import APIRouter, HTTPException
from utils.scraper import scrape_templates
from database import get_templates
import asyncio

router = APIRouter()

@router.get("/templates")
async def search_templates(query: str):
    templates = get_templates(query)
    
    if not templates:
        await scrape_templates(query)
        templates = get_templates(query)
    
    if not templates:
        raise HTTPException(status_code=404, detail="No templates found.")

    return {"results": [{"title": t[1], "description": t[2], "thumbnail": t[3], "url": t[4]} for t in templates]}