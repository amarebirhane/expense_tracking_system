# backend/app/services/insights.py
from sklearn.linear_model import LinearRegression
import numpy as np
from ....db.models.expense import Expense
from sqlalchemy.orm import Session

def get_spending_trends(db: Session, owner_id: int, months: int = 6):
    # Fetch last months expenses
    expenses = db.query(Expense).filter(Expense.owner_id == owner_id).order_by(Expense.date).all()
    # Simple linear regression for forecast
    dates = np.array([exp.date.toordinal() for exp in expenses]).reshape(-1, 1)
    amounts = np.array([exp.amount for exp in expenses])
    model = LinearRegression().fit(dates, amounts)
    future_dates = np.array([[dates[-1][0] + 30 * i] for i in range(1, months+1)])
    forecast = model.predict(future_dates)
    return {"forecast": forecast.tolist()}

# Anomaly detection: simple duplicate check
def detect_anomalies(expenses: List[Expense]):
    seen = set()
    anomalies = []
    for exp in expenses:
        key = (exp.date, exp.amount, exp.notes)
        if key in seen:
            anomalies.append(exp.id)
        seen.add(key)
    return anomalies