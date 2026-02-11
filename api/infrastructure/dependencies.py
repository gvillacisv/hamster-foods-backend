from fastapi import Depends

from api.application.ports import CustomerRepository, CurrencyConverter
from api.application.currency_service import StaticCurrencyConverter
from api.application.customer_service import CustomerTierService
from api.infrastructure.db_repository import SqliteCustomerRepository


def get_customer_repository() -> CustomerRepository:
    return SqliteCustomerRepository()

def get_currency_converter() -> CurrencyConverter:
    return StaticCurrencyConverter()

def get_customer_tier_service(
    customer_repository: CustomerRepository = Depends(get_customer_repository),
    currency_converter: CurrencyConverter = Depends(get_currency_converter)
) -> CustomerTierService:

    return CustomerTierService(
        customer_repository=customer_repository,
        currency_converter=currency_converter
    )
