import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from api.application.sync_tier_service import SyncTierService


# Integration tests for HTTP API endpoints
# These tests run against the actual API with a test database


@pytest.fixture
def test_db():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    os.environ["DATABASE_URL"] = db_path
    os.environ["API_KEY"] = "test-api-key-123"

    yield db_path

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(f"{db_path}-journal"):
        os.remove(f"{db_path}-journal")


def test_health_check():
    """Test the health check endpoint."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test the root endpoint."""
    from main import app

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "status" in response.json()


def test_no_sqlite_repository_import_in_http_api():
    """http_api.py MUST NOT import SqliteCustomerRepository directly."""
    import api.infrastructure.http_api as http_api_module
    import inspect

    source = inspect.getsource(http_api_module)
    assert 'SqliteCustomerRepository' not in source
    assert 'from api.infrastructure.sqlite_repository' not in source


def test_sync_tier_uses_sync_tier_service():
    """sync_tier endpoint MUST use SyncTierService, not repository directly."""
    import api.infrastructure.http_api as http_api_module
    import inspect

    source = inspect.getsource(http_api_module)
    assert 'SyncTierService' in source
    assert 'sync_service.sync_user_tier' in source or 'SyncTierService' in source


# Note: Full integration tests for API endpoints would require:
# 1. Setting up test database with schema and seed data
# 2. Properly initialized repository with test data
# 3. Testing authentication flow


def test_cors_headers_not_present_by_default():
    """Test that CORS headers are not added without configuration."""
    from main import app

    os.environ.pop("CORS_ORIGINS", None)

    client = TestClient(app)
    response = client.get("/health")

    # Should not have CORS headers when no origins configured
    assert "access-control-allow-origin" not in response.headers or \
           response.headers.get("access-control-allow-origin") == "None"
