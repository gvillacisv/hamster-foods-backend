from fastapi import APIRouter, HTTPException, status, Depends, Query

from api.application.customer_service import CustomerTierService, CustomerNotFound
from api.domain.models import CustomerTierStatusResponse, SyncTierRequest
from api.infrastructure.dependencies import get_customer_tier_service, get_customer_repository
from api.infrastructure.db_repository import SqliteCustomerRepository


router = APIRouter()

@router.get(
    "/customers/{customer_id}/tier-status",
    response_model=CustomerTierStatusResponse,
    tags=["Tiers"],
    summary="Get customer's current tier status"
)
def get_tier_status(
    customer_id: str,
    target_currency: str = Query('EUR', description="The target currency for all monetary values (e.g., EUR, GBP, USD)."),
    service: CustomerTierService = Depends(get_customer_tier_service)
):
    try:
        return service.get_customer_tier_status(customer_id, target_currency)
    except CustomerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/customers/{customer_id}/sync-tier",
    status_code=status.HTTP_200_OK,
    tags=["Tiers"],
    summary="Trigger a manual tier synchronization for a customer"
)
def sync_tier(
    customer_id: str,
    request: SyncTierRequest,
    repository: SqliteCustomerRepository = Depends(get_customer_repository)
):
    try:
        repository.sync_user_tier(customer_id, request.reason)

        return {"status": "success", "message": f"Tier synchronization completed for customer {customer_id}."}
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync tier for customer {customer_id}: {str(exception)}"
        )
