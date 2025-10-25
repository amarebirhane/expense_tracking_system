# backend/app/schemas/user.py (updated with Login model)
from pydantic import BaseModel, EmailStr
from typing import Optional
from ..db.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[Role] = Role.EMPLOYEE

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Login(BaseModel):
    username: str
    password: str