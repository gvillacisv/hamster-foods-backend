from .models import Tier
from typing import Optional

TIER_THRESHOLDS: dict[Tier, float] = {
    Tier.CHAMPION: 23,
    Tier.LOYAL: 15,
    Tier.ROOKIE: 7,
    Tier.NO_TIER: 0,
}

def get_tier_for_amount(amount: float, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> Tier:
    sorted_tiers_desc = sorted(thresholds.items(), key=lambda item: item[1], reverse=True)
    for tier, threshold_val in sorted_tiers_desc:
        if amount >= threshold_val:
            return tier
    return Tier.NO_TIER

def get_next_tier_info(amount: float, current_tier: Tier, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> tuple[Optional[Tier], float]:
    if current_tier == Tier.CHAMPION:
        return None, 0.0

    current_threshold = thresholds[current_tier]
    next_tier_threshold = float('inf')
    next_tier_candidate = None

    for tier, threshold in thresholds.items():
        if threshold > current_threshold:
            if threshold < next_tier_threshold:
                next_tier_threshold = threshold
                next_tier_candidate = tier
    
    if next_tier_candidate is None:
        return None, 0.0

    amount_needed = next_tier_threshold - amount
    return next_tier_candidate, round(amount_needed, 2) if amount_needed > 0 else 0.0

def calculate_tier_progress(current_total: float, current_tier: Tier, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> tuple[float, float]:
    is_champion = current_tier == Tier.CHAMPION
    max_threshold = max(thresholds.values())
    
    if is_champion or max_threshold == 0:
        return 100.0 if is_champion else 0.0, max_threshold

    progress_percentage = (current_total / max_threshold) * 100
    percentage = round(min(progress_percentage, 100), 2)

    return percentage, max_threshold