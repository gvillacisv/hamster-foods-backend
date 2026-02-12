from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from api.domain.constants import Tier


class TierHistoryItem(BaseModel):
    id: str
    tier: Tier
    date: datetime
    total_base_at_change: float = Field(alias='totalAtChange')
    change_reason: str = Field(alias='changeReason')

    class Config:
        populate_by_name = True

class CustomerTierStatusResponse(BaseModel):
    customer_id: str = Field(alias='customerId')
    customer_name: str = Field(alias='customerName')
    current_tier: Tier = Field(alias='currentTier')
    current_total: float = Field(alias='currentTotal')
    display_currency: str = Field(alias='displayCurrency')
    amount_to_next_tier: float = Field(alias='amountToNextTier')
    next_tier: Optional[Tier] = Field(alias='nextTier', default=None)
    overall_progress_percentage: float = Field(alias='overallProgressPercentage')
    top_tier_threshold: float = Field(alias='topTierThreshold')
    tier_history: list[TierHistoryItem] = Field(alias='tierHistory')

    class Config:
        populate_by_name = True

class Order(BaseModel):
    id: str
    customer_id: str
    amount_value: float
    amount_currency: str
    amount_base: float
    exchange_rate: float
    created_at: datetime

class Customer(BaseModel):
    id: str
    name: str

class SyncTierRequest(BaseModel):
    reason: str
    order_id: Optional[str] = Field(default=None, alias='orderId')

    class Config:
        populate_by_name = True