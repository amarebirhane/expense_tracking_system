# backend/app/api/v1/endpoints/admin.py (fix imports: get_current_user from deps, Role from models)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import get_users
from app.db.session import get_db
from app.api.deps import get_current_user
from app.db.models.user import User, Role

router = APIRouter(prefix="/admin", tags=["admin"])

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@router.get("/users")
def list_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    users = get_users(db)
    return [{"id": u.id, "email": u.email, "role": u.role.value} for u in users]