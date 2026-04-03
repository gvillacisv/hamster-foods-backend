import os
from typing import List, Optional


def get_cors_origins() -> List[str]:
    """
    Get CORS origins from environment variable.
    Set CORS_ORIGINS as comma-separated list (e.g., http://localhost:3000,https://example.com)
    Leave empty for production (no CORS).
    """
    cors_env = os.getenv("CORS_ORIGINS", "")
    if not cors_env:
        return []
    return [origin.strip() for origin in cors_env.split(",") if origin.strip()]


def get_database_url() -> str:
    """Get database path from environment or use default."""
    return os.getenv("DATABASE_URL", "tier_status.db")


def get_api_key() -> Optional[str]:
    """Get API key for authentication."""
    return os.getenv("API_KEY")


def is_debug_mode() -> bool:
    """Check if running in debug mode."""
    return os.getenv("DEBUG", "false").lower() == "true"


def get_rate_limit() -> int:
    """Get rate limit per minute."""
    return int(os.getenv("RATE_LIMIT", "100"))