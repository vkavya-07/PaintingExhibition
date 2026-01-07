from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["health"])

START_TIME = datetime.now(timezone.utc)

@router.get("/", summary="Health check")
def health_check():
    """Returns basic health information."""
    uptime = (datetime.now(timezone.utc) - START_TIME).total_seconds()
    return {"status": "ok", "uptime": uptime}