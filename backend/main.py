from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from .routes import ingest, generate, debug
import asyncio
import sys

# Fix for Playwright on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

app = FastAPI(
    title="AutoDoc AI API",
    description="API for AutoDoc AI - Automatic Documentation Generator",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Frontend
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(generate.router, prefix="/api/v1")
app.include_router(debug.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to AutoDoc AI API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
