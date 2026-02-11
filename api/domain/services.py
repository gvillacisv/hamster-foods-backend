from typing import Optional

from api.domain.constants import Tier, TIER_THRESHOLDS


def get_tier_for_amount(amount: float, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> Tier:
    listed_thresholds = thresholds.items()

    for tier, threshold in listed_thresholds:
        if amount >= threshold:
            return tier

    return Tier.NO_TIER

def get_next_tier_info(current_total: float, current_tier: Tier, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> tuple[Optional[Tier], float]:
    if current_tier == Tier.CHAMPION:
        return None, 0.0

    listed_thresholds = list(thresholds.items())
    current_tier_index = -1

    for index, (tier, _) in enumerate(listed_thresholds):
        if tier == current_tier:
            current_tier_index = index

            break

    next_tier, next_tier_threshold = listed_thresholds[current_tier_index - 1]
    amount_needed = next_tier_threshold - current_total

    return next_tier, round(amount_needed, 2)

def calculate_tier_progress(current_total: float, current_tier: Tier, thresholds: dict[Tier, float] = TIER_THRESHOLDS) -> tuple[float, float]:
    top_tier_threshold = thresholds[Tier.CHAMPION]

    if current_tier == Tier.CHAMPION:
        return 100.0, top_tier_threshold

    progress = (current_total / top_tier_threshold) * 100

    return round(min(progress, 100.0), 2), top_tier_threshold
