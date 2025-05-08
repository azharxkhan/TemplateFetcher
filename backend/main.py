from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import templates

app = FastAPI()

# Allow frontend (localhost:3000) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(templates.router)
