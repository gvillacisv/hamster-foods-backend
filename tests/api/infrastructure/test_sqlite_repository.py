from datetime import datetime
from unittest.mock import patch

from api.domain.constants import Tier


def test_get_customer_by_id(database, repository):
    database.fetchone.return_value = {'id': 'c-01', 'name': 'Test Customer'}

    customer = repository.get_customer_by_id('c-01')

    database.execute.assert_called_once_with(
        "SELECT id, name FROM customers WHERE id = ?", ('c-01',)
    )

    assert customer.name == 'Test Customer'


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


def test_get_current_tier_with_history(database, repository):
    """get_current_tier returns (Tier, total) when history exists."""
    database.fetchone.return_value = {'tier': 'Rookie', 'total_base_at_change': 10.0}

    tier, total = repository.get_current_tier('c-01')

    assert tier == Tier.ROOKIE
    assert total == 10.0


def test_get_current_tier_no_history(database, repository):
    """get_current_tier returns (NO_TIER, -1.0) when no history."""
    database.fetchone.return_value = None

    tier, total = repository.get_current_tier('c-01')

    assert tier == Tier.NO_TIER
    assert total == -1.0


def test_get_order_total_since(database, repository):
    """get_order_total_since returns rounded sum."""
    database.fetchone.return_value = {'total': 25.5}

    total = repository.get_order_total_since('c-01', datetime(2023, 10, 1))

    assert total == 25.5


def test_get_order_total_since_no_orders(database, repository):
    """get_order_total_since returns 0.0 when no orders."""
    database.fetchone.return_value = {'total': None}

    total = repository.get_order_total_since('c-01', datetime(2023, 10, 1))

    assert total == 0.0


def test_insert_tier_history(database, repository):
    """insert_tier_history inserts a record via SQL."""
    record = {
        'id': 'th-01',
        'customer_id': 'c-01',
        'order_id': 'o-01',
        'tier': 'Rookie',
        'date': '2023-10-10T10:00:00',
        'total_base_at_change': 10.0,
        'change_reason': 'TRANSACTION'
    }

    repository.insert_tier_history(record)

    args, _ = database.execute.call_args
    assert "INSERT INTO tier_history" in args[0]
    assert args[1] == ('th-01', 'c-01', 'o-01', 'Rookie', '2023-10-10T10:00:00', 10.0, 'TRANSACTION')


def test_tier_already_synced_for_order_true(database, repository):
    """tier_already_synced_for_order returns True when row exists."""
    database.fetchone.return_value = (1,)

    result = repository.tier_already_synced_for_order('o-01')

    assert result is True


def test_tier_already_synced_for_order_false(database, repository):
    """tier_already_synced_for_order returns False when no row."""
    database.fetchone.return_value = None

    result = repository.tier_already_synced_for_order('o-01')

    assert result is False


def test_get_customer_by_id_not_found(database, repository):
    """get_customer_by_id returns None when customer does not exist."""
    database.fetchone.return_value = None

    customer = repository.get_customer_by_id('nonexistent')

    assert customer is None


def test_get_tier_history_desc(database, repository):
    """get_tier_history_desc returns tier history ordered by date desc."""
    database.fetchall.return_value = [
        {
            'id': 'th-02', 'tier': 'Champion', 'date': '2023-11-01T10:00:00',
            'total_base_at_change': 25.0, 'change_reason': 'TRANSACTION'
        },
        {
            'id': 'th-01', 'tier': 'Rookie', 'date': '2023-10-01T10:00:00',
            'total_base_at_change': 7.5, 'change_reason': 'TRANSACTION'
        },
    ]

    history = repository.get_tier_history_desc('c-01')

    assert len(history) == 2
    assert history[0].tier == Tier.CHAMPION
    assert history[0].id == 'th-02'
    assert history[1].tier == Tier.ROOKIE
    assert history[1].id == 'th-01'

    database.execute.assert_called_once()
    args, _ = database.execute.call_args
    assert "ORDER BY date DESC" in args[0]


def test_get_tier_history_desc_empty(database, repository):
    """get_tier_history_desc returns empty list when no history."""
    database.fetchall.return_value = []

    history = repository.get_tier_history_desc('c-01')

    assert history == []


def test_get_db_connection():
    """get_db_connection returns a sqlite3 connection with Row factory."""
    from api.infrastructure.sqlite_repository import get_db_connection
    import tempfile
    import os as os_mod

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        with patch('api.infrastructure.sqlite_repository.get_database_url', return_value=db_path):
            conn = get_db_connection()
            assert conn is not None
            # Verify row_factory is set to Row
            import sqlite3
            assert conn.row_factory == sqlite3.Row
            conn.close()
    finally:
        if os_mod.path.exists(db_path):
            os_mod.remove(db_path)
