from fastapi import FastAPI
from api.infrastructure.http_api import router as api_router

app = FastAPI(
    title="Hamster Foods Tier API",
    description="API for calculating and querying customer loyalty tiers.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to the Hamster Foods Tier API!"}