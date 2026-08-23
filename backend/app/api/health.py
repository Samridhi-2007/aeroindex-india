from fastapi import APIRouter

from app.core.config import HealthResponse, Settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = Settings()
    return HealthResponse(status="ok", service=settings.app_name)
