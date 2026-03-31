import pytest

from api.application.currency_service import StaticCurrencyConverter
from api.application.ports import CurrencyConverter


def test_currency_converter_abc_exists():
    """CurrencyConverter ABC must exist with abstract convert method."""
    assert issubclass(StaticCurrencyConverter, CurrencyConverter)
    converter = StaticCurrencyConverter()
    assert hasattr(converter, 'convert')
    assert callable(converter.convert)


@pytest.mark.parametrize("amount, from_currency, to_currency, expected_amount", [
    (100, 'EUR', 'EUR', 100),
    (100, 'EUR', 'GBP', 84.75),
    (100, 'EUR', 'USD', 107.53),
])
def test_static_currency_converter_same_currency(amount, from_currency, to_currency, expected_amount):
    converter = StaticCurrencyConverter()
    assert converter.convert(amount, from_currency, to_currency) == expected_amount


@pytest.mark.parametrize("amount, from_currency, to_currency", [
    (100, 'JPY', 'EUR'),
    (100, 'EUR', 'JPY')
])
def test_static_currency_converter_unsupported_currency(amount, from_currency, to_currency):
    converter = StaticCurrencyConverter()
    with pytest.raises(ValueError):
        converter.convert(amount, from_currency, to_currency)


def test_static_currency_converter_case_insensitive():
    converter = StaticCurrencyConverter()
    assert converter.convert(100, 'eur', 'eur') == 100
    assert converter.convert(100, 'Eur', 'GBP') == 84.75
