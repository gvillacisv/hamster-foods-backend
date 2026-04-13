import os
import logging
from pathlib import Path
from typing import List
from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file if it exists
from dotenv import load_dotenv

# Try to load .env file from various locations
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)
load_dotenv()  # Also check current directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from api.infrastructure.http_api import router as api_router
from api.infrastructure.config import get_cors_origins

app = FastAPI(
    title="Tier Status API",
    description="API for calculating and querying customer loyalty tiers.",
    version="1.0.0"
)

# Get CORS origins from environment (comma-separated list)
# Default to empty list for production - add origins via CORS_ORIGINS env var
origins = get_cors_origins()

# Only add CORS middleware if origins are configured
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to the Tier Status API!"}


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}