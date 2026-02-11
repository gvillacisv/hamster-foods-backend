from datetime import datetime, timedelta

import api.domain.services as domain_services
from api.application.ports import CustomerRepository, CurrencyConverter
from api.domain.constants import BASE_CURRENCY
from api.domain.models import CustomerTierStatusResponse


class CustomerNotFound(Exception):
    pass

class CustomerTierService:
    def __init__(self, customer_repository: CustomerRepository, currency_converter: CurrencyConverter):
        self._customer_repository = customer_repository
        self._currency_converter = currency_converter

    def get_customer_tier_status(self, customer_id: str, target_currency: str) -> CustomerTierStatusResponse:
        customer = self._customer_repository.get_customer_by_id(customer_id)

        if not customer:
            raise CustomerNotFound(f"Customer with id {customer_id} not found.")

        ten_days_ago = datetime.now() - timedelta(days=10)
        recent_orders = self._customer_repository.get_orders_for_customer_since(customer_id, ten_days_ago)
        current_total = sum(order.amount_base for order in recent_orders)

        tier_history = self._customer_repository.get_tier_history_desc(customer_id)
        current_tier = tier_history[0].tier if tier_history else domain_services.get_tier_for_amount(current_total)

        target_currency_upper = target_currency.upper()
        current_total_display = round(self._currency_converter.convert(current_total, BASE_CURRENCY, target_currency_upper), 2)

        next_tier, amount_to_next_tier = domain_services.get_next_tier_info(current_total, current_tier)
        amount_to_next_tier_display = round(self._currency_converter.convert(amount_to_next_tier, BASE_CURRENCY, target_currency_upper), 2)

        tier_progress, top_tier_threshold_base = domain_services.calculate_tier_progress(current_total, current_tier)
        top_tier_threshold_display = round(self._currency_converter.convert(top_tier_threshold_base, BASE_CURRENCY, target_currency_upper), 2)

        return CustomerTierStatusResponse(
            customerId=customer.id,
            customerName=customer.name,
            currentTier=current_tier,
            currentTotal=current_total_display,
            displayCurrency=target_currency_upper,
            amountToNextTier=amount_to_next_tier_display,
            nextTier=next_tier,
            overallProgressPercentage=tier_progress,
            topTierThreshold=top_tier_threshold_display,
            tierHistory=tier_history
        )
