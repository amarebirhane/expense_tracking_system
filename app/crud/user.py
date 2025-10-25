# backend/app/crud/user.py
from sqlalchemy.orm import Session
from typing import Optional
from ..core.security import get_password_hash, verify_password
from ..schemas.user import UserCreate, UserUpdate
from ..db.models.user import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    db_user = User(email=user_create.email, hashed_password=hashed_password, role=user_create.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Add update_user, get_users, etc.
def get_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user