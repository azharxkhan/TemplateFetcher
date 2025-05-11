from fastapi import FastAPI
from routers import templates

app = FastAPI()

app.include_router(templates.router, prefix="/api")
