from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from api.domain.models import Customer, Order, TierHistoryItem


class CustomerRepository(ABC):

    @abstractmethod
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def get_orders_for_customer_since(self, customer_id: str, date_from: datetime) -> list[Order]:
        raise NotImplementedError
        
    @abstractmethod
    def get_tier_history_desc(self, customer_id: str) -> list[TierHistoryItem]:
        raise NotImplementedError
