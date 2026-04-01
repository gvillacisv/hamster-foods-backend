import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional

import api.domain.services as domain_services
from api.application.ports import CustomerRepository

logger = logging.getLogger(__name__)


class SyncTierService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    def sync_user_tier(self, customer_id: str, reason: str, order_id: Optional[str] = None):
        if order_id and self._customer_repository.tier_already_synced_for_order(order_id):
            return

        current_tier, last_recorded_total = self._customer_repository.get_current_tier(customer_id)

        ten_days_ago = datetime.now() - timedelta(days=10)
        current_total = self._customer_repository.get_order_total_since(customer_id, ten_days_ago)

        new_tier = domain_services.get_tier_for_amount(current_total)
        should_insert = (
            new_tier != current_tier or
            last_recorded_total < 0 or
            (reason == 'TRANSACTION' and current_total != last_recorded_total)
        )

        if should_insert:
            self._customer_repository.insert_tier_history({
                'id': f"th-{customer_id}-{uuid.uuid4().hex[:10]}",
                'customer_id': customer_id,
                'order_id': order_id,
                'tier': new_tier.value,
                'date': datetime.now().isoformat(),
                'total_base_at_change': current_total,
                'change_reason': reason
            })
