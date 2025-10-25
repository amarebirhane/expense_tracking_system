# backend/app/api/v1/endpoints/auth.py (add import for User)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import authenticate_user, create_user, get_user_by_email
from app.schemas.user import UserCreate, Login
from app.core.security import create_access_token
from app.db.session import get_db
from app.core.config import settings
from app.api.deps import get_current_active_user
from app.db.models.user import User  # Add this import
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user_create=user_create)

@router.post("/login")
def login(login_data: Login, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {"email": current_user.email, "role": current_user.role.value, "id": current_user.id}