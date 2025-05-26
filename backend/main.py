from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_templates

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/templates")
def search_templates(query: str = Query(..., min_length=1)):
    templates = get_templates(query)
    if not templates:
        raise HTTPException(status_code=404, detail="No templates found.")
    return {"results": templates}
