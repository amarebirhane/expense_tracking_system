# backend/app/services/reports.py (fix relative import to 2 dots)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from openpyxl import Workbook
from ..db.models.expense import Expense  # Changed to .. (2 dots)
from typing import List

def generate_pdf_report(expenses: List[Expense]) -> str:
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Expense Report")
    y = 700
    for exp in expenses:
        p.drawString(100, y, f"{exp.date}: {exp.category.value} - ${exp.amount}")
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750
    p.save()
    buffer.seek(0)
    pdf_path = 'report.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    return pdf_path

def generate_excel_report(expenses: List[Expense]) -> str:
    wb = Workbook()
    ws = wb.active
    ws.append(['Date', 'Category', 'Amount'])
    for exp in expenses:
        ws.append([exp.date.isoformat(), exp.category.value, exp.amount])
    excel_path = 'report.xlsx'
    wb.save(excel_path)
    return excel_path