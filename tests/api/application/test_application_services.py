import pytest
from unittest.mock import MagicMock

from api.application.services import CustomerTierService, CustomerNotFound
from api.domain.constants import Tier
from api.domain.models import Customer


def test_get_customer_tier_status_not_found():
    mock_customer_repository = MagicMock()
    mock_currency_converter = MagicMock()

    mock_customer_repository.get_customer_by_id.return_value = None

    service = CustomerTierService(mock_customer_repository, mock_currency_converter)

    with pytest.raises(CustomerNotFound):
        service.get_customer_tier_status('c1', 'EUR')

def test_get_customer_tier_status_success(champion_fixture):
    mock_customer_repository = MagicMock()
    mock_currency_converter = MagicMock()

    fixture = champion_fixture

    mock_customer_repository.get_customer_by_id.return_value = fixture['customer']
    mock_customer_repository.get_orders_for_customer_since.return_value = fixture['orders']
    mock_customer_repository.get_tier_history_desc.return_value = fixture['history']
    mock_currency_converter.convert.side_effect = lambda amount, _, __: amount * 1

    target = CustomerTierService(mock_customer_repository, mock_currency_converter)

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
    mock_currency_converter = MagicMock()

    fixture = newcomer_fixture

    mock_customer_repository.get_customer_by_id.return_value = fixture['customer']
    mock_customer_repository.get_orders_for_customer_since.return_value = fixture['orders']
    mock_customer_repository.get_tier_history_desc.return_value = fixture['history']
    mock_currency_converter.convert.side_effect = lambda amount, _, __: amount * 1

    target = CustomerTierService(mock_customer_repository, mock_currency_converter)

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
