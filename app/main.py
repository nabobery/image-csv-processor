from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import upload, status, webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

def create_app() -> FastAPI:
    app_ = FastAPI(lifespan=lifespan)
    # Include routers
    app_.include_router(upload.router, prefix="/api/v1", tags=["upload"])
    app_.include_router(status.router, prefix="/api/v1", tags=["status"])
    app_.include_router(webhook.router, prefix="/api/v1", tags=["webhook"])
    return app_

app = create_app()