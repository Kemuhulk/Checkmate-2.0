import tempfile
import streamlit as st
import os
from PIL import Image
from api.gemini_api import analyze_check_with_gemini
from database.db_manager import store_cheque_data
from extract.extract_text import convert_pdf_to_images, save_images

import streamlit as st
st.set_page_config(page_title="Cheque Processing", page_icon="📄")

if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")

st.title("📄 Upload and Process a Cheque")

STORAGE_PATH = "stored_cheques"

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

def main():
    uploaded_file = st.file_uploader("Upload Cheque (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file:
        st.text("Processing cheque...")

        image_path = None  # Initialize image path

        # Handle PDF upload
        if uploaded_file.type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.getbuffer())
                pdf_path = temp_pdf.name

            images = convert_pdf_to_images(pdf_path)  # Convert PDF to images

            if not images:
                st.error("No images extracted from the PDF.")
                return

            image_paths = save_images(images)  # Save extracted images
            
            if not image_paths:
                st.error("Failed to save extracted images from PDF.")
                return
            
            image_path = image_paths[0]  # Pick the first extracted image (ensure it's an image)
            st.write("Extracted image path:", image_path)

        else:
            # Save uploaded cheque image directly
            image_path = os.path.join(STORAGE_PATH, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Ensure the file is an image before opening it
        try:
            if image_path and image_path.lower().endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(image_path)
                st.image(image, caption="Uploaded Cheque")
            else:
                st.error("The extracted file is not a valid image.")
                return
        except Exception as e:
            st.error(f"Error opening image: {e}")
            return

        # Process cheque image with Gemini
        structured_data = analyze_check_with_gemini(image_path=image_path)
        status = structured_data.get("Status")  

        # Determine status if not provided
        if not status:      
            if "Not Found" in structured_data.values():  
                status = "Failed"
            else:
                status = "Successful"  

        structured_data["Status"] = status  

        st.write("Structured Data:", structured_data)

        # Store cheque details in database
        store_cheque_data(uploaded_file.name, structured_data)

        st.success("Cheque data saved successfully!")

if __name__ == "__main__":
    main()

