# backend/app/db/models/approval.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.base_class import BaseDB
from datetime import datetime

class Approval(BaseDB):
    __tablename__ = "approvals"

    expense_id = Column(Integer, ForeignKey("expenses.id"), unique=True)
    approver_id = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime, default=datetime.utcnow)
    comments = Column(String, nullable=True)

    expense = relationship("Expense", back_populates="approval")
    approver = relationship("User", back_populates="approvals")