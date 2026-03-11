import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes import chat, health

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Create FastAPI app
app = FastAPI(
    title="AI Assistant API",
    description="Backend API for the AI Assistant chatbot",
    version="1.0.0"
)

# Configure CORS for React frontend
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = [
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    return {"message": "AI Assistant API", "docs": "/docs"}
