import os
import tempfile
import pytest
from fastapi.testclient import TestClient


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


# Note: Full integration tests for API endpoints would require:
# 1. Setting up test database with schema and seed data
# 2. Properly initialized repository with test data  
# 3. Testing authentication flow
# 
# Example test structure:
# def test_get_tier_status_with_auth(test_db):
#     os.environ["API_KEY"] = "test-api-key"
#     from main import app
#     
#     client = TestClient(app)
#     
#     # Request with valid API key
#     response = client.get(
#         "/api/v1/customers/c-01/tier-status",
#         headers={"X-API-Key": "test-api-key"}
#     )
#     
#     # Either succeeds or returns 404 if customer not in test DB
#     assert response.status_code in [200, 404]
#     
#     # Request without API key when API_KEY is configured
#     response = client.get("/api/v1/customers/c-01/tier-status")
#     assert response.status_code in [200, 401]


def test_cors_headers_not_present_by_default():
    """Test that CORS headers are not added without configuration."""
    from main import app
    
    os.environ.pop("CORS_ORIGINS", None)
    
    client = TestClient(app)
    response = client.get("/health")
    
    # Should not have CORS headers when no origins configured
    assert "access-control-allow-origin" not in response.headers or \
           response.headers.get("access-control-allow-origin") == "None"