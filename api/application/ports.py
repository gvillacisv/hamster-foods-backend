from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from api.domain.models import Customer, Order, TierHistoryItem


class CurrencyConverter(ABC):

    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        raise NotImplementedError


class CustomerQueryPort(ABC):

    @abstractmethod
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def get_orders_for_customer_since(self, customer_id: str, date_from: datetime) -> list[Order]:
        raise NotImplementedError
        
    @abstractmethod
    def get_tier_history_desc(self, customer_id: str) -> list[TierHistoryItem]:
        raise NotImplementedError


class TierMutationPort(ABC):

    @abstractmethod
    def get_current_tier(self, customer_id: str) -> tuple:
        """Returns (Tier, last_recorded_total: float) or (Tier.NO_TIER, -1.0) if no history."""
        raise NotImplementedError

    @abstractmethod
    def get_order_total_since(self, customer_id: str, date_from: datetime) -> float:
        raise NotImplementedError

    @abstractmethod
    def insert_tier_history(self, record: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def tier_already_synced_for_order(self, order_id: str) -> bool:
        raise NotImplementedError


# Backward compatibility: CustomerRepository combines both ports
class CustomerRepository(CustomerQueryPort, TierMutationPort):
    pass
