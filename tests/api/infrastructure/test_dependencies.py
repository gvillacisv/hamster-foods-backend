from unittest.mock import MagicMock

from api.application.customer_service import CustomerTierService
from api.application.sync_tier_service import SyncTierService
from api.application.currency_service import StaticCurrencyConverter
from api.application.ports import CurrencyConverter
from api.infrastructure.sqlite_repository import SqliteCustomerRepository
from api.infrastructure.dependencies import (
    get_customer_repository,
    get_currency_converter,
    get_customer_tier_service,
    get_sync_tier_service
)


def test_get_customer_repository_returns_correct_type():
    repository = get_customer_repository()

    assert isinstance(repository, SqliteCustomerRepository)


def test_get_currency_converter_returns_static_converter():
    converter = get_currency_converter()

    assert isinstance(converter, StaticCurrencyConverter)
    assert isinstance(converter, CurrencyConverter)


def test_get_sync_tier_service_exists():
    """get_sync_tier_service factory function must exist."""
    mock_repo = MagicMock()

    service = get_sync_tier_service(customer_repository=mock_repo)

    assert isinstance(service, SyncTierService)


def test_get_customer_tier_service_with_converter():
    """get_customer_tier_service injects both repository and currency converter."""
    mock_repo = MagicMock()
    mock_converter = MagicMock(spec=CurrencyConverter)

    service = get_customer_tier_service(
        customer_repository=mock_repo,
        currency_converter=mock_converter
    )

    assert isinstance(service, CustomerTierService)
    assert service._customer_repository == mock_repo
    assert service._currency_converter == mock_converter
