from datetime import datetime
from unittest.mock import patch

from api.domain.constants import Tier


def test_get_customer_by_id(database, repository):
    database.fetchone.return_value = {'id': 'c-01', 'name': 'Hamster King'}

    customer = repository.get_customer_by_id('c-01')

    database.execute.assert_called_once_with(
        "SELECT id, name FROM customers WHERE id = ?", ('c-01',)
    )

    assert customer.name == 'Hamster King'

def test_get_orders_for_customer_since(database, repository):
    database.fetchall.return_value = [
        {
            'id': 'o1', 'customer_id': 'c1', 'amount_value': 10, 
            'amount_currency': 'EUR', 'amount_base': 10, 
            'exchange_rate': 1, 'created_at': '2023-10-10 10:00:00'
        }
    ]
    
    date_from = datetime(2023, 10, 1)
    orders = repository.get_orders_for_customer_since('c1', date_from)
    
    expected_date_str = '2023-10-01 00:00:00'
    args, _ = database.execute.call_args
    assert expected_date_str in args[1]
    assert len(orders) == 1

@patch('api.domain.services.get_tier_for_amount')
def test_sync_user_tier_no_change(mock_get_tier, database, repository):
    """Tests that no INSERT happens if the tier remains the same."""
    database.fetchone.side_effect = [
        {'tier': 'Rookie'},
        {'total': 10.0}
    ]
    mock_get_tier.return_value = Tier.ROOKIE

    repository.sync_user_tier('c-01', 'Regular update')

    for call in database.execute.call_args_list:
        assert "INSERT INTO tier_history" not in call[0][0]

@patch('api.domain.services.get_tier_for_amount')
def test_sync_user_tier_with_change(mock_get_tier, database, repository):
    """Tests that INSERT is called when the tier changes."""
    database.fetchone.side_effect = [
        {'tier': 'Rookie'},
        {'total': 100.0}
    ]
    mock_get_tier.return_value = Tier.CHAMPION

    repository.sync_user_tier('c-01', 'Rank up')

    insert_called = any("INSERT INTO tier_history" in call[0][0] for call in database.execute.call_args_list)
    assert insert_called is True
