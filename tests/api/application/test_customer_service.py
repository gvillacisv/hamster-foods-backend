import pytest
from unittest.mock import MagicMock

from api.application.customer_service import CustomerTierService, CustomerNotFound
from api.application.currency_service import StaticCurrencyConverter
from api.application.ports import CurrencyConverter
from api.domain.constants import Tier


def test_customer_tier_service_injects_currency_converter():
    """CustomerTierService constructor must accept CurrencyConverter."""
    mock_repo = MagicMock()
    mock_converter = MagicMock(spec=CurrencyConverter)
    service = CustomerTierService(mock_repo, mock_converter)
    assert service._currency_converter is mock_converter


def test_get_customer_tier_status_not_found():
    mock_customer_repository = MagicMock()
    mock_converter = StaticCurrencyConverter()

    mock_customer_repository.get_customer_by_id.return_value = None

    service = CustomerTierService(mock_customer_repository, mock_converter)

    with pytest.raises(CustomerNotFound):
        service.get_customer_tier_status('c1', 'EUR')


def test_get_customer_tier_status_success(champion_fixture):
    mock_customer_repository = MagicMock()
    mock_converter = StaticCurrencyConverter()

    fixture = champion_fixture

    mock_customer_repository.get_customer_by_id.return_value = fixture['customer']
    mock_customer_repository.get_orders_for_customer_since.return_value = fixture['orders']
    mock_customer_repository.get_tier_history_desc.return_value = fixture['history']

    target = CustomerTierService(mock_customer_repository, mock_converter)

    result = target.get_customer_tier_status('c-01', 'EUR')

    assert result.customer_id == 'c-01'
    assert result.customer_name == 'Champion'
    assert result.current_tier == Tier.CHAMPION
    assert result.current_total == 25.0
    assert result.display_currency == 'EUR'
    assert result.next_tier == None
    assert result.amount_to_next_tier == 0.0
    assert result.overall_progress_percentage == 100.0
    assert result.top_tier_threshold == 23.0


def test_get_customer_tier_status_no_history(newcomer_fixture):
    mock_customer_repository = MagicMock()
    mock_converter = StaticCurrencyConverter()

    fixture = newcomer_fixture

    mock_customer_repository.get_customer_by_id.return_value = fixture['customer']
    mock_customer_repository.get_orders_for_customer_since.return_value = fixture['orders']
    mock_customer_repository.get_tier_history_desc.return_value = fixture['history']

    target = CustomerTierService(mock_customer_repository, mock_converter)

    result = target.get_customer_tier_status('c-01', 'EUR')

    assert result.customer_id == 'c-02'
    assert result.customer_name == 'Newcomer'
    assert result.current_tier == Tier.NO_TIER
    assert result.current_total == 0.0
    assert result.display_currency == 'EUR'
    assert result.next_tier == Tier.ROOKIE
    assert result.amount_to_next_tier == 7.0
    assert result.overall_progress_percentage == 0.0
    assert result.top_tier_threshold == 23.0


def test_get_customer_tier_status_uses_injected_converter():
    """Verify CustomerTierService uses currency_converter.convert() not bare convert()."""
    from api.domain.models import Customer

    mock_customer_repository = MagicMock()
    mock_converter = MagicMock(spec=CurrencyConverter)

    mock_customer_repository.get_customer_by_id.return_value = Customer(id='c-01', name='Test')
    mock_customer_repository.get_orders_for_customer_since.return_value = []
    mock_customer_repository.get_tier_history_desc.return_value = []

    mock_converter.convert.return_value = 0.0

    service = CustomerTierService(mock_customer_repository, mock_converter)
    service.get_customer_tier_status('c-01', 'EUR')

    assert mock_converter.convert.called
