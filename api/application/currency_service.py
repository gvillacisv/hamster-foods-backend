from api.domain.constants import RATES_TO_BASE

def convert(amount: float, from_currency: str, to_currency: str) -> float:
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()

    if from_curr not in RATES_TO_BASE or to_curr not in RATES_TO_BASE:
        raise ValueError(f"One of the currencies is not supported: {from_currency}, {to_currency}")
    
    if from_curr == to_curr:
        return amount

    amount_in_base = amount * RATES_TO_BASE[from_curr]
    amount_in_target = amount_in_base / RATES_TO_BASE[to_curr]

    return round(amount_in_target, 2)
