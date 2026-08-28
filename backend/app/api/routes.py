from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.airfare import router as airfare_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(airfare_router, prefix="/api/v1")

