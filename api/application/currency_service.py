from api.application.ports import CurrencyConverter

class StaticCurrencyConverter(CurrencyConverter):

    _rates_to_base = {
        "EUR": 1.0,
        "GBP": 1.18,
        "USD": 0.93,
    }

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()

        if from_curr not in self._rates_to_base or to_curr not in self._rates_to_base:
            raise ValueError(f"One of the currencies is not supported: {from_currency}, {to_currency}")
        
        if from_curr == to_curr:
            return amount

        amount_in_base = amount * self._rates_to_base[from_curr]
        amount_in_target = amount_in_base / self._rates_to_base[to_curr]

        return round(amount_in_target, 2)
