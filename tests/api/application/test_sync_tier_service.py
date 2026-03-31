from unittest.mock import MagicMock, patch

from api.application.sync_tier_service import SyncTierService
from api.domain.constants import Tier


def test_sync_tier_service_calls_repository_methods():
    """SyncTierService.sync_user_tier orchestrates via repository ports."""
    mock_repo = MagicMock()

    mock_repo.tier_already_synced_for_order.return_value = False
    mock_repo.get_current_tier.return_value = (Tier.ROOKIE, 10.0)
    mock_repo.get_order_total_since.return_value = 25.0

    service = SyncTierService(mock_repo)
    service.sync_user_tier('c-01', 'TRANSACTION', order_id='o-01')

    mock_repo.tier_already_synced_for_order.assert_called_once_with('o-01')
    mock_repo.get_current_tier.assert_called_once_with('c-01')
    mock_repo.get_order_total_since.assert_called_once()
    mock_repo.insert_tier_history.assert_called_once()


def test_sync_tier_service_skips_if_already_synced():
    """If order already synced, no further calls are made."""
    mock_repo = MagicMock()

    mock_repo.tier_already_synced_for_order.return_value = True

    service = SyncTierService(mock_repo)
    service.sync_user_tier('c-01', 'TRANSACTION', order_id='o-01')

    mock_repo.get_current_tier.assert_not_called()
    mock_repo.get_order_total_since.assert_not_called()
    mock_repo.insert_tier_history.assert_not_called()


def test_sync_tier_service_inserts_on_tier_change():
    """When tier changes, insert_tier_history is called."""
    mock_repo = MagicMock()

    mock_repo.tier_already_synced_for_order.return_value = False
    mock_repo.get_current_tier.return_value = (Tier.NO_TIER, -1.0)
    mock_repo.get_order_total_since.return_value = 10.0

    service = SyncTierService(mock_repo)
    service.sync_user_tier('c-01', 'TRANSACTION')

    mock_repo.insert_tier_history.assert_called_once()
    call_args = mock_repo.insert_tier_history.call_args[0][0]
    assert call_args['customer_id'] == 'c-01'
    assert call_args['tier'] == Tier.ROOKIE.value
    assert call_args['change_reason'] == 'TRANSACTION'


def test_sync_tier_service_no_insert_when_no_change():
    """When tier and total haven't changed, no insert occurs."""
    mock_repo = MagicMock()

    mock_repo.tier_already_synced_for_order.return_value = False
    mock_repo.get_current_tier.return_value = (Tier.ROOKIE, 10.0)
    mock_repo.get_order_total_since.return_value = 10.0

    service = SyncTierService(mock_repo)
    service.sync_user_tier('c-01', 'EXPIRATION')

    mock_repo.insert_tier_history.assert_not_called()


def test_sync_tier_service_inserts_on_transaction_total_change():
    """TRANSACTION reason with different total triggers insert even if tier same."""
    mock_repo = MagicMock()

    mock_repo.tier_already_synced_for_order.return_value = False
    mock_repo.get_current_tier.return_value = (Tier.ROOKIE, 8.0)
    mock_repo.get_order_total_since.return_value = 10.0

    service = SyncTierService(mock_repo)
    service.sync_user_tier('c-01', 'TRANSACTION')

    mock_repo.insert_tier_history.assert_called_once()
