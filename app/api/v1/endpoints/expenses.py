# backend/app/api/v1/endpoints/expenses.py (ensure async def and imports)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.crud.expense import create_expense, get_expenses
from app.schemas.expense import ExpenseCreate, Expense
from app.services.ocr import extract_from_receipt
from app.services.ai_categorization import categorizer
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.expense import Category, ExpenseStatus
from app.api.deps import get_current_user
from fastapi import status

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=Expense)
async def create_new_expense(  # Ensure 'async' here
    expense_in: ExpenseCreate,
    receipt: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ocr_data = {}
    if receipt:
        contents = await receipt.read()
        ocr_data = extract_from_receipt(contents)
        if ocr_data.get("amount"):
            expense_in.amount = float(ocr_data["amount"])
        if ocr_data.get("date"):
            try:
                expense_in.date = datetime.fromisoformat(ocr_data["date"])
            except ValueError:
                expense_in.date = datetime.now()
        expense_in.notes = ocr_data.get("text", "")
        predicted_category = categorizer.categorize(ocr_data.get("text", ""))
        expense_in.category = Category(predicted_category)
    return create_expense(db=db, expense_create=expense_in, owner_id=current_user.id)

@router.get("/", response_model=List[Expense])
def read_expenses(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_expenses(db, skip=skip, limit=limit, owner_id=current_user.id)