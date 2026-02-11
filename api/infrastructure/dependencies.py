from fastapi import Depends

from api.application.ports import CustomerRepository
from api.application.customer_service import CustomerTierService
from api.infrastructure.sqlite_repository import SqliteCustomerRepository


def get_customer_repository() -> CustomerRepository:
    return SqliteCustomerRepository()

def get_customer_tier_service(
    customer_repository: CustomerRepository = Depends(get_customer_repository),
) -> CustomerTierService:

    return CustomerTierService(customer_repository=customer_repository)
