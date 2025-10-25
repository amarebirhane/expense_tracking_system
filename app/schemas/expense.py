# backend/app/schemas/expense.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..db.models.expense import Category, PaymentMethod, ExpenseStatus

class ExpenseBase(BaseModel):
    amount: float
    category: Category
    payment_method: PaymentMethod
    project: Optional[str] = None
    date: datetime
    notes: Optional[str] = None
    is_recurring: bool = False

class ExpenseCreate(ExpenseBase):
    currency: str = "USD"

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[Category] = None
    # ... other optional fields

class Expense(ExpenseBase):
    id: int
    currency: str
    status: ExpenseStatus
    owner_id: int
    receipt_url: Optional[str] = None

    class Config:
        from_attributes = True