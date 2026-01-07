from fastapi import FastAPI
from app.db import init_db
from app.api.paintings.routes import router as paintings_router
from app.api.health.routes import router as health_router

app = FastAPI(title="Painting Exhibition API")

app.include_router(paintings_router)
app.include_router(health_router)

@app.on_event("startup")
def on_startup():
    init_db()