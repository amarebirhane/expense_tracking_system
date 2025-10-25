# backend/app/crud/expense.py
from sqlalchemy.orm import Session
from ..schemas.expense import ExpenseCreate, ExpenseUpdate
from ..db.models.expense import Expense

def create_expense(db: Session, expense_create: ExpenseCreate, owner_id: int) -> Expense:
    db_expense = Expense(**expense_create.dict(), owner_id=owner_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, skip: int = 0, limit: int = 100, owner_id: int = None):
    query = db.query(Expense)
    if owner_id:
        query = query.filter(Expense.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

# Add get_expense, update_expense, delete_expense, etc.