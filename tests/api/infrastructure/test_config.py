import os
import pytest
from unittest.mock import patch

from api.infrastructure.config import (
    get_cors_origins,
    get_database_url,
    get_api_key,
    is_debug_mode,
    get_rate_limit,
)


def test_get_cors_origins_empty_when_not_set():
    """Returns empty list when CORS_ORIGINS is not set."""
    with patch.dict(os.environ, {}, clear=True):
        result = get_cors_origins()
        assert result == []


def test_get_cors_origins_parses_comma_separated():
    """Parses comma-separated origins, stripping whitespace."""
    with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000, https://example.com , http://other.com"}):
        result = get_cors_origins()
        assert result == ["http://localhost:3000", "https://example.com", "http://other.com"]


def test_get_database_url_uses_env():
    """Returns DATABASE_URL from environment when set."""
    with patch.dict(os.environ, {"DATABASE_URL": "/tmp/test.db"}):
        assert get_database_url() == "/tmp/test.db"


def test_get_database_url_default():
    """Returns default path when DATABASE_URL is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert get_database_url() == "hamster_foods.db"


def test_get_api_key_returns_none_when_not_set():
    """Returns None when API_KEY env is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert get_api_key() is None


def test_get_api_key_returns_value_when_set():
    """Returns API_KEY from environment when set."""
    with patch.dict(os.environ, {"API_KEY": "my-secret"}):
        assert get_api_key() == "my-secret"


def test_is_debug_mode_true():
    """Returns True when DEBUG=true."""
    with patch.dict(os.environ, {"DEBUG": "true"}):
        assert is_debug_mode() is True


def test_is_debug_mode_case_insensitive():
    """DEBUG value is case-insensitive."""
    with patch.dict(os.environ, {"DEBUG": "TRUE"}):
        assert is_debug_mode() is True


def test_is_debug_mode_false():
    """Returns False when DEBUG is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert is_debug_mode() is False


def test_is_debug_mode_false_when_other_value():
    """Returns False when DEBUG is something other than 'true'."""
    with patch.dict(os.environ, {"DEBUG": "0"}):
        assert is_debug_mode() is False


def test_get_rate_limit_default():
    """Returns default rate limit of 100 when RATE_LIMIT is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert get_rate_limit() == 100


def test_get_rate_limit_from_env():
    """Returns RATE_LIMIT from environment when set."""
    with patch.dict(os.environ, {"RATE_LIMIT": "50"}):
        assert get_rate_limit() == 50
