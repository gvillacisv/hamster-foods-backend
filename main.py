from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.infrastructure.http_api import router as api_router

app = FastAPI(
    title="Hamster Foods Tier API",
    description="API for calculating and querying customer loyalty tiers.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to the Hamster Foods Tier API!"}