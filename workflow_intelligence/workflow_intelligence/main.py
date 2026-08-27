
from fastapi import FastAPI

from .database import Base, engine
from . import models
from .api.routes import router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AtSpeed Workflow Intelligence Service",
    description="Risk-aware work queue service for operational work items.",
    version="1.0.0"
)


# Register API routes
app.include_router(
    router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "service": "AtSpeed Workflow Intelligence Service",
        "version": "1.0.0",
        "docs": "/docs"
    }
