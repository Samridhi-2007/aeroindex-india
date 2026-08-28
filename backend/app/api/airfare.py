from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query, BackgroundTasks


from app.services.airfare_service import AirfareService

router = APIRouter(prefix="/airfare", tags=["airfare"])
service = AirfareService()


@router.get("/summary")
def get_summary() -> Dict[str, Any]:
    """Get high-level Airfare Price Index summary, change, status, and observation counts."""
    return service.get_summary()


@router.get("/index")
def get_index() -> Dict[str, Any]:
    """Get the full APIx report including index, route components, and confidence scores."""
    return service.get_latest_report()


@router.get("/routes")
def get_routes() -> List[Dict[str, Any]]:
    """Get route-level elementary indices, representative fares, and route weights."""
    return service.get_routes()


@router.get("/observations")
def get_observations(
    limit: int = Query(100, ge=1, le=1000),
    period: Optional[str] = Query(None, description="Filter by 'base' or 'current' period"),
) -> List[Dict[str, Any]]:
    """Get raw & clean fare observations from source storage."""
    return service.get_observations(limit=limit, period=period)


@router.get("/quality")
def get_quality() -> Dict[str, Any]:
    """Get data quality score, 7-component confidence breakdown, and validation issues."""
    return service.get_quality()


@router.get("/status")
def get_status() -> Dict[str, Any]:
    """Get system and pipeline status (calculation status, weighting status, timestamps)."""
    return service.get_status()


@router.get("/metadata")
def get_metadata() -> Dict[str, Any]:
    """Get methodology, version metadata, and CPI Airfare weight provenance."""
    return service.get_metadata()


@router.post("/collect")
def post_collect() -> Dict[str, Any]:
    """Trigger recalculation and persist report in results storage."""
    return service.recalculate_report()

