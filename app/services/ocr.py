# backend/app/services/ocr.py
import pytesseract
from PIL import Image
from io import BytesIO

def extract_from_receipt(image_bytes: bytes) -> dict:
    image = Image.open(BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    # Simple parsing: assume lines like "Total: $XX.XX"
    lines = text.split('\n')
    amount = None
    date = None
    for line in lines:
        if 'total' in line.lower() and '$' in line:
            # Simple extraction - adjust as needed
            try:
                amount = float(line.split('$')[-1].split()[0].replace(',', ''))
            except ValueError:
                pass
        if '/' in line and len(line.split('/')) == 3:  # Assume date MM/DD/YYYY
            date = line.strip().split()[0]
    return {"text": text, "amount": amount, "date": date}