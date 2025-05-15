import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_NAME="checkmate_db"
DB_USER="postgres"
DB_PASSWORD="12345"
DB_HOST="localhost"
DB_PORT="5432"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
