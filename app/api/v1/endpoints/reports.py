# backend/app/api/v1/endpoints/reports.py (fix relative import to absolute)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.session import get_db
from app.db.models.expense import Expense
from app.services.reports import generate_pdf_report, generate_excel_report
from app.api.deps import get_current_user
from app.db.models.user import User
from fastapi.responses import FileResponse
from datetime import datetime
from fastapi import status

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/pdf")
def export_pdf(
    start_date: str,
    end_date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
    expenses = db.query(Expense).filter(
        Expense.owner_id == current_user.id,
        Expense.date >= start,
        Expense.date <= end
    ).all()
    pdf_path = generate_pdf_report(expenses)
    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename='expense_report.pdf'
    )

@router.get("/excel")
def export_excel(
    start_date: str,
    end_date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
    expenses = db.query(Expense).filter(
        Expense.owner_id == current_user.id,
        Expense.date >= start,
        Expense.date <= end
    ).all()
    excel_path = generate_excel_report(expenses)
    return FileResponse(
        path=excel_path,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename='expense_report.xlsx'
    )

@router.get("/dashboard")
def get_dashboard_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total = db.query(func.sum(Expense.amount)).filter(Expense.owner_id == current_user.id).scalar() or 0
    category_breakdown = db.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(Expense.owner_id == current_user.id).group_by(Expense.category).all()
    categories = [{"name": cat[0].value, "amount": float(cat[1] or 0)} for cat in category_breakdown]
    return {"total": float(total), "categories": categories}