# backend/app/__init__.py (corrected import for Base)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.api import api_router
from .db.session import engine
from .db.base import Base  

app = FastAPI(title="Intelligent Expense Tracking System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Uncomment to auto-create tables on startup (for development; use Alembic for production)
# Base.metadata.create_all(bind=engine)