from enum import Enum


class Tier(str, Enum):
    CHAMPION = 'Champion'
    LOYAL = 'Loyal'
    ROOKIE = 'Rookie'
    NO_TIER = 'No Tier'

BASE_CURRENCY: str = 'EUR'

RATES_TO_BASE = {
    "EUR": 1.0,
    "GBP": 1.18,
    "USD": 0.93,
}

# Sorted reversed manually to simplify Tier calculations
TIER_THRESHOLDS: dict[Tier, float] = {
    Tier.CHAMPION: 23,
    Tier.LOYAL: 15,
    Tier.ROOKIE: 7,
    Tier.NO_TIER: 0,
}
