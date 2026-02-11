import pytest

from api.domain.constants import Tier
from api.domain.services import get_tier_for_amount, get_next_tier_info, calculate_tier_progress


@pytest.mark.parametrize("amount, expected_tier", [
    (-5, Tier.NO_TIER),
    (0, Tier.NO_TIER),
    (6.99, Tier.NO_TIER),
    (7, Tier.ROOKIE),
    (14.99, Tier.ROOKIE),
    (15, Tier.LOYAL),
    (22.99, Tier.LOYAL),
    (23, Tier.CHAMPION),
    (100, Tier.CHAMPION)
])
def test_get_tier_for_amount(amount, expected_tier):
    assert get_tier_for_amount(amount) == expected_tier

@pytest.mark.parametrize("current_total, current_tier, expected_next_tier, expected_amount_needed", [
    (6.99, Tier.NO_TIER, Tier.ROOKIE, 0.01),
    (12.53, Tier.ROOKIE, Tier.LOYAL, 2.47),
    (20.0, Tier.LOYAL, Tier.CHAMPION, 3.0),
    (25.7, Tier.CHAMPION, None, 0.0)
])
def test_get_next_tier_info(current_total, current_tier, expected_next_tier, expected_amount_needed):
    next_tier, amount_needed = get_next_tier_info(current_total, current_tier)

    assert next_tier == expected_next_tier
    assert amount_needed == expected_amount_needed
    
@pytest.mark.parametrize("current_total, current_tier, expected_percentage", [
    (0, Tier.NO_TIER, 0.0),
    (11.5, Tier.ROOKIE, 50.0),
    (23, Tier.LOYAL, 100.0),
    (30, Tier.CHAMPION, 100.0)
])
def test_calculate_tier_progress(current_total, current_tier, expected_percentage):
    percentage, top_tier_threshold = calculate_tier_progress(current_total, current_tier)

    assert percentage == expected_percentage
    assert top_tier_threshold == 23
