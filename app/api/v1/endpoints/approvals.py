# backend/app/api/v1/endpoints/approvals.py (update import to absolute)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.approval import create_approval  # Absolute import
from app.api.deps import get_current_user
from app.db.models.user import User, Role
from app.db.models.expense import ExpenseStatus

router = APIRouter(prefix="/approvals", tags=["approvals"])

@router.post("/{expense_id}/approve")
def approve_expense(
    expense_id: int,
    comments: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in [Role.MANAGER, Role.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to approve")
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.status == ExpenseStatus.PENDING).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or not pending")
    approval = create_approval(db, expense_id, current_user.id, comments)
    if approval:
        return {"message": "Expense approved successfully"}
    raise HTTPException(status_code=500, detail="Failed to approve expense")