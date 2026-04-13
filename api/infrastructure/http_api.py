from fastapi import APIRouter, HTTPException, status, Depends, Query

from api.application.customer_service import CustomerTierService, CustomerNotFound
from api.application.sync_tier_service import SyncTierService
from api.domain.models import CustomerTierStatusResponse, SyncTierRequest
from api.infrastructure.dependencies import get_customer_tier_service, get_sync_tier_service
from api.infrastructure.auth import require_api_key
from api.infrastructure.config import get_api_key


router = APIRouter()


def get_auth_dependency():
    """Get authentication dependency based on API key configuration."""
    api_key = get_api_key()
    if api_key is None or api_key == "":
        # No API key configured - auth disabled (dev mode)
        return lambda: None
    return require_api_key


# Get the appropriate auth dependency
require_auth = get_auth_dependency()


@router.get(
    "/customers/{customer_id}/tier-status",
    response_model=CustomerTierStatusResponse,
    tags=["Tiers"],
    summary="Get customer's current tier status"
)
def get_tier_status(
    customer_id: str,
    target_currency: str = Query('EUR', description="The target currency for all monetary values (e.g., EUR, GBP, USD)."),
    service: CustomerTierService = Depends(get_customer_tier_service),
    _: None = Depends(require_auth)
):
    """
    Get customer's current tier status.

    Requires API key authentication if API_KEY is configured.
    """
    try:
        return service.get_customer_tier_status(customer_id, target_currency)
    except CustomerNotFound as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exception))


@router.post(
    "/customers/{customer_id}/sync-tier",
    status_code=status.HTTP_200_OK,
    tags=["Tiers"],
    summary="Trigger a manual tier synchronization for a customer"
)
def sync_tier(
    customer_id: str,
    request: SyncTierRequest,
    sync_service: SyncTierService = Depends(get_sync_tier_service),
    _: None = Depends(require_auth)
):
    """
    Trigger a manual tier synchronization for a customer.

    Requires API key authentication if API_KEY is configured.
    """
    try:
        sync_service.sync_user_tier(customer_id, request.reason, request.order_id)

        return {"status": "success", "message": f"Tier synchronization completed for customer {customer_id}."}
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync tier for customer {customer_id}: {str(exception)}"
        )
