import pytest
from unittest.mock import MagicMock

from api.application.customer_service import CustomerTierService
from api.infrastructure.sqlite_repository import SqliteCustomerRepository
from api.infrastructure.dependencies import (
    get_customer_repository,
    get_customer_tier_service
)

def test_get_customer_repository_returns_correct_type():
    repository = get_customer_repository()

    assert isinstance(repository, SqliteCustomerRepository)

def test_get_customer_tier_service():
    repository_mock = MagicMock()

    service = get_customer_tier_service(repository_mock)

    assert isinstance(service, CustomerTierService)
    assert service._customer_repository == repository_mock
