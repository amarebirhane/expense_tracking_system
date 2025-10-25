# backend/app/db/models/expense.py (add Integer to import)
from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Text, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import BaseDB
from enum import Enum as PyEnum
from datetime import datetime

class Category(str, PyEnum):
    TRAVEL = "travel"
    MEALS = "meals"
    OFFICE_SUPPLIES = "office_supplies"
    OTHER = "other"

class PaymentMethod(str, PyEnum):
    CASH = "cash"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"

class ExpenseStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REIMBURSED = "reimbursed"

class Expense(BaseDB):
    __tablename__ = "expenses"

    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    category = Column(SQLEnum(Category), nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    project = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    receipt_url = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(SQLEnum(ExpenseStatus), default=ExpenseStatus.PENDING)

    owner = relationship("User", back_populates="expenses")
    approval = relationship("Approval", back_populates="expense", uselist=False)