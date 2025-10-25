# backend/app/db/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from ..base_class import BaseDB
from enum import Enum as PyEnum

class Role(str, PyEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class User(BaseDB):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.EMPLOYEE)
    phone = Column(String, nullable=True)  # For OTP

    expenses = relationship("Expense", back_populates="owner")
    approvals = relationship("Approval", back_populates="approver")