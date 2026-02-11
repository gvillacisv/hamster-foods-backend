import pytest

from api.application.currency_service import convert

@pytest.mark.parametrize("amount, from_currency, to_currency, expected_amount", [
    (100, 'EUR','EUR', 100),
    (100, 'EUR', 'GBP', 84.75),
    (100, 'EUR', 'USD', 107.53),
])
def test_convert_same_currency(amount, from_currency, to_currency, expected_amount):
    assert convert(amount, from_currency, to_currency) == expected_amount

@pytest.mark.parametrize("amount, from_currency, to_currency", [
    (100, 'JPY','EUR'),
    (100, 'EUR', 'JPY')
])
def test_unsupported_currency(amount, from_currency, to_currency):
    with pytest.raises(ValueError):
        convert(amount, from_currency, to_currency)
