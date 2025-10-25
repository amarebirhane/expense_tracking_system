# backend/app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import auth, expenses, reports, approvals, admin

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(expenses.router)
api_router.include_router(reports.router)
api_router.include_router(approvals.router)
api_router.include_router(admin.router)