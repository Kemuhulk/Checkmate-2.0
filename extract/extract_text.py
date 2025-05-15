import pdf2image
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import numpy as np
import tempfile
import os
from config import TESSERACT_PATH, POPPLER_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"

def convert_pdf_to_images(pdf_path):
    """Convert each page of a PDF into images."""
    try:
        if not os.path.exists(pdf_path):
            raise Exception(f"PDF file not found: {pdf_path}")

        if os.path.getsize(pdf_path) == 0:
            raise Exception(f"PDF file is empty: {pdf_path}")

        print(f"Using Poppler Path: {POPPLER_PATH}")  # Debugging output
        print(f"Processing PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")

        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

        if not images:
            raise Exception(f"No images extracted from PDF: {pdf_path}")

        return images
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {e}")


def preprocess_image(image):
    """Enhance cheque image for better OCR accuracy."""
    try:
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        # Apply Adaptive Thresholding for better text contrast
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Morphological Transformations to remove noise
        kernel = np.ones((2,2), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return Image.fromarray(processed)

    except Exception as e:
        raise Exception(f"Error in preprocessing: {e}")

def convert_pdf_to_images(pdf_path):
    """Convert each page of a PDF into images."""
    try:
        if not os.path.exists(pdf_path):
            raise Exception(f"PDF file not found: {pdf_path}")

        if os.path.getsize(pdf_path) == 0:
            raise Exception(f"PDF file is empty: {pdf_path}")

        print(f"Using Poppler Path: {POPPLER_PATH}")  # Debugging output
        print(f"Processing PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")

        images = pdf2image.convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

        if not images:
            raise Exception(f"No images extracted from PDF: {pdf_path}")

        return images
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {e}")

def save_images(images):
    """Save converted images to temporary files and return their paths."""
    temp_image_paths = []
    for i, img in enumerate(images):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(temp_file.name, format="JPEG")
        temp_image_paths.append(temp_file.name)
    return temp_image_paths
    
def extract_text_from_image(image):
    """Extract text from an image using OCR."""
    try:
        processed_image = preprocess_image(image)  # Apply preprocessing
        text = pytesseract.image_to_string(processed_image, config="--psm 6")  
        return text.strip() if text.strip() else "No text found."
    except Exception as e:
        raise Exception(f"Error processing image: {e}")
