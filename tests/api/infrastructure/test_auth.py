import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from api.infrastructure.auth import APIKeyValidator, require_api_key, api_key_validator


class TestAPIKeyValidator:
    """Tests for APIKeyValidator.get_api_key behavior."""

    def test_returns_key_when_api_key_not_configured(self):
        """When API_KEY env is not set, auth is disabled and key passes through."""
        validator = APIKeyValidator.__new__(APIKeyValidator)
        validator.api_key = None

        result = validator.get_api_key("any-key")
        assert result == "any-key"

    def test_returns_key_when_api_key_not_configured_and_none_header(self):
        """When API_KEY env is not set, even None header passes through."""
        validator = APIKeyValidator.__new__(APIKeyValidator)
        validator.api_key = None

        result = validator.get_api_key(None)
        assert result is None

    def test_raises_401_when_key_required_but_missing(self):
        """When API_KEY is configured and header is None, raise 401."""
        validator = APIKeyValidator.__new__(APIKeyValidator)
        validator.api_key = "secret-123"

        with pytest.raises(HTTPException) as exc_info:
            validator.get_api_key(None)

        assert exc_info.value.status_code == 401
        assert "missing" in exc_info.value.detail.lower()

    def test_raises_403_when_key_is_wrong(self):
        """When API_KEY is configured and header doesn't match, raise 403."""
        validator = APIKeyValidator.__new__(APIKeyValidator)
        validator.api_key = "secret-123"

        with pytest.raises(HTTPException) as exc_info:
            validator.get_api_key("wrong-key")

        assert exc_info.value.status_code == 403
        assert "invalid" in exc_info.value.detail.lower()

    def test_returns_key_when_valid(self):
        """When API_KEY is configured and header matches, return it."""
        validator = APIKeyValidator.__new__(APIKeyValidator)
        validator.api_key = "secret-123"

        result = validator.get_api_key("secret-123")
        assert result == "secret-123"


class TestRequireApiKey:
    """Tests for the require_api_key dependency function."""

    def test_require_api_key_delegates_to_validator(self):
        """require_api_key must call api_key_validator.get_api_key."""
        with patch.object(api_key_validator, 'get_api_key', return_value='validated') as mock:
            result = require_api_key("test-key")
            mock.assert_called_once_with("test-key")
            assert result == "validated"
