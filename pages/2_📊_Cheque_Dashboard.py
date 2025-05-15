import os
from PIL import Image, UnidentifiedImageError
import streamlit as st
import pandas as pd
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

IMAGE_FOLDER = "stored_cheques/"

def is_image_file(filename):
    """Check if the file is an image based on extension."""
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))

def display_image(image_path, filename):
    """Safely display an image, avoiding non-image files like PDFs."""
    if not is_image_file(filename):  # Ignore PDFs
        return  
    
    if os.path.exists(image_path):
        try:
            image = Image.open(image_path)  # Open as image safely
            st.image(image, caption=filename, width=150)
        except UnidentifiedImageError:
            st.warning(f"⚠️ File '{filename}' is not a valid image.")
        except Exception as e:
            st.warning(f"⚠️ Cannot display image '{filename}'. Error: {e}")
    else:
        st.warning(f"⚠️ Image file not found: {filename}")

# Fetch cheques from the database
def fetch_cheques():
    """Fetch cheque data from the database."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, payee, amount_words, amount_digits, bank, ifsc_code,
               account_number, cheque_number, cheque_date, signature_verification, processed_at
        FROM cheques ORDER BY processed_at DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    columns = ["id", "filename", "payee", "amount_words", "amount_digits", "bank",
               "ifsc_code", "account_number", "cheque_number", "cheque_date",
               "signature_verification", "processed_at"]
    
    return pd.DataFrame(data, columns=columns)

# Delete a cheque record
def delete_cheque(cheque_id):
    """Deletes a cheque from the database using its unique ID."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cheques WHERE id = %s;", (cheque_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting cheque: {e}")
        return False

def main():
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")

    st.title("📊 Cheque Dashboard")
    st.subheader("Uploaded Cheque Records")
    
    cheques_df = fetch_cheques()
    
    if cheques_df.empty:
        st.warning("No cheques uploaded yet!")
        return

    # Display DataFrame
    st.dataframe(cheques_df, use_container_width=True)

    # CSV Download Option
    csv = cheques_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="cheque_data.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.subheader("🗑 Delete a Cheque Record")
    
    # Select cheque ID for deletion
    cheque_ids = cheques_df["id"].dropna().astype(str).tolist()
    if cheque_ids:
        selected_cheque_id = st.selectbox("Select a cheque ID to delete:", cheque_ids)

        # Warning before deletion
        st.warning(f"⚠️ You are about to delete cheque ID **{selected_cheque_id}**. This action is irreversible!")

        # Confirmation checkbox
        confirm_delete = st.checkbox("Yes, I want to delete this cheque")

        # Delete Button (only works if confirmed)
        if st.button("❌ Delete Selected Cheque", disabled=not confirm_delete):
            if delete_cheque(selected_cheque_id):
                st.success(f"✅ Cheque with ID {selected_cheque_id} deleted successfully!")
                st.rerun()  # Refreshes the page after deletion
    else:
        st.warning("No valid cheque IDs found for deletion.")

    st.markdown("---")
    
    st.write("### Uploaded Cheques")

    for index, row in cheques_df.iterrows():
        image_path = os.path.join(IMAGE_FOLDER, row["filename"])
        
        # Skip non-image files
        if not is_image_file(row["filename"]):
            continue
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            display_image(image_path, row["filename"])  # Safe image loading

        with col2:
            st.write(f"**Payee:** {row['payee']}")
            st.write(f"**Amount:** {row['amount_words']} ({row['amount_digits']})")
            st.write(f"**Bank:** {row['bank']}")
            st.write(f"**Cheque Number:** {row['cheque_number']}")
            st.write("---")

if __name__ == "__main__":
    main()
