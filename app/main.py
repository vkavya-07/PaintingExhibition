import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.db import init_db
from app.api.paintings.routes import router as paintings_router
from app.api.health.routes import router as health_router

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("paintingexhibition")

app = FastAPI(
    title="Painting Exhibition API",
    version="0.1.0",
    description="API for managing a painting gallery. Supports role-based operations for `user` and `admin` roles.",
    contact={"name": "PaintingExhibition Maintainer"},
)

app.include_router(paintings_router)
app.include_router(health_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response {response.status_code} for {request.method} {request.url}")
        return response
    except Exception as exc:
        logger.exception(f"Unhandled error processing request {request.method} {request.url}: {exc}")
        raise

@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root to the interactive Swagger UI."""
    return RedirectResponse(url="/docs")

@app.on_event("startup")
def on_startup():
    logger.info("Initializing database and application startup")
    init_db()
    logger.info("Startup complete")