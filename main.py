# backend/main.py
import warnings
from app import app

# Suppress Pydantic alias warning
warnings.filterwarnings("ignore", message=".*'alias' attribute.*")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)