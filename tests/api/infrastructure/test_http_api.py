import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from api.application.sync_tier_service import SyncTierService
from api.application.customer_service import CustomerTierService, CustomerNotFound
from api.application.ports import CustomerRepository, CurrencyConverter


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


@pytest.fixture
def mock_services():
    """Fixture to override dependencies with mocks."""
    from main import app
    from api.infrastructure.dependencies import (
        get_customer_tier_service,
        get_sync_tier_service,
    )

    mock_repo = MagicMock(spec=CustomerRepository)
    mock_currency = MagicMock(spec=CurrencyConverter)
    mock_tier_service = MagicMock(spec=CustomerTierService)
    mock_sync_service = MagicMock(spec=SyncTierService)

    app.dependency_overrides[get_customer_tier_service] = lambda: mock_tier_service
    app.dependency_overrides[get_sync_tier_service] = lambda: mock_sync_service

    yield mock_tier_service, mock_sync_service

    app.dependency_overrides.clear()


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


# Error handler tests for coverage

def test_get_tier_status_returns_404_when_customer_not_found(mock_services):
    """get_tier_status MUST return 404 when CustomerNotFound is raised."""
    from main import app

    mock_tier_service, _ = mock_services
    mock_tier_service.get_customer_tier_status.side_effect = CustomerNotFound("customer-123")

    client = TestClient(app)
    os.environ["API_KEY"] = "test-api-key-123"
    response = client.get(
        "/api/v1/customers/customer-123/tier-status",
        headers={"X-API-Key": "test-api-key-123"}
    )

    assert response.status_code == 404
    assert "customer-123" in response.json()["detail"]


def test_get_tier_status_returns_500_on_generic_exception(mock_services):
    """get_tier_status MUST return 500 when unexpected exception is raised."""
    from main import app

    mock_tier_service, _ = mock_services
    mock_tier_service.get_customer_tier_status.side_effect = RuntimeError("Database error")

    client = TestClient(app)
    os.environ["API_KEY"] = "test-api-key-123"
    response = client.get(
        "/api/v1/customers/customer-123/tier-status",
        headers={"X-API-Key": "test-api-key-123"}
    )

    assert response.status_code == 500
    assert "Database error" in response.json()["detail"]


def test_sync_tier_returns_500_on_generic_exception(mock_services):
    """sync_tier MUST return 500 when unexpected exception is raised."""
    from main import app
    from api.application.sync_tier_service import SyncTierService as STS

    mock_tier_service, mock_sync_service = mock_services
    mock_sync_service.sync_user_tier.side_effect = RuntimeError("Sync failed")

    client = TestClient(app)
    os.environ["API_KEY"] = "test-api-key-123"
    response = client.post(
        "/api/v1/customers/customer-123/sync-tier",
        json={"reason": "manual", "order_id": "order-456"},
        headers={"X-API-Key": "test-api-key-123"}
    )

    assert response.status_code == 500
    assert "Failed to sync tier" in response.json()["detail"]
