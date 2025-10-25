# backend/app/crud/approval.py
from sqlalchemy.orm import Session
from typing import Optional
from app.db.models.approval import Approval
from app.db.models.expense import Expense
from app.db.models.user import User
from app.db.models.expense import ExpenseStatus
from app.services.notifications import send_email

def create_approval(db: Session, expense_id: int, approver_id: int, comments: str = "") -> Optional[Approval]:
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return None
    approval = Approval(expense_id=expense_id, approver_id=approver_id, comments=comments)
    db.add(approval)
    expense.status = ExpenseStatus.APPROVED
    db.commit()
    db.refresh(approval)
    # Send notification
    if expense.owner:
        send_email(expense.owner.email, "Expense Approved", f"Your expense {expense_id} has been approved.\nComments: {comments}")
    return approval

def get_approval(db: Session, approval_id: int) -> Optional[Approval]:
    return db.query(Approval).filter(Approval.id == approval_id).first()

def get_approvals_by_user(db: Session, approver_id: int):
    return db.query(Approval).filter(Approval.approver_id == approver_id).all()