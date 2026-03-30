import os
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader


class APIKeyValidator:
    """Validates API key from Authorization header."""

    def __init__(self):
        self.api_key: Optional[str] = os.getenv("API_KEY")
        self.header_name = os.getenv("API_KEY_HEADER", "X-API-Key")
        self._security = APIKeyHeader(name=self.header_name, auto_error=False)

    def get_api_key(self, api_key_header: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))) -> str:
        """Validate the API key from request header."""
        if self.api_key is None:
            # API key not configured - authentication disabled
            return api_key_header

        if api_key_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key is missing"
            )

        if api_key_header != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key"
            )

        return api_key_header


# Global instance
api_key_validator = APIKeyValidator()


def require_api_key(api_key: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))) -> str:
    """
    Dependency to require API key authentication.
    Use this in FastAPI endpoints that need protection.
    """
    return api_key_validator.get_api_key(api_key)