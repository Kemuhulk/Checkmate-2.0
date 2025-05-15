import streamlit as st
import psycopg2
import pandas as pd
from io import BytesIO
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Function to fetch data from PostgreSQL
def fetch_data():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    query = "SELECT * FROM cheques;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load data
df = fetch_data()
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")
st.title("📂 Export Cheque Data")

# Custom CSS for buttons (Card Style)
st.markdown(
    """
    <style>
        .stDownloadButton {
            width: 270px !important;
            height: 120px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            font-size: 20px !important;
            font-weight: bold !important;
            background-color: #1f1f1f !important;
            color: white !important;
            border-radius: 15px !important;
            text-align: center !important;
            cursor: pointer !important;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s ease-in-out !important;
        }
        .stDownloadButton:hover {
            transform: scale(1.05) !important;
            box-shadow: 4px 4px 15px rgba(255, 255, 255, 0.4) !important;
        }
        .button-container {
            display: flex;
            justify-content: space-around;
            gap: 40px; /* Adjust gap between buttons */
            margin-top: 20px; /* Add space between title and buttons */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Convert data into different formats
csv_data = df.to_csv(index=False).encode("utf-8")
json_data = df.to_json(indent=4).encode("utf-8")

# Convert DataFrame to Excel
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

# Center the buttons with spacing
st.markdown('<div class="button-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="cheque_data.csv",
        mime="text/csv",
    )

with col2:
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="cheque_data.json",
        mime="application/json",
    )

with col3:
    st.download_button(
        label="Download Excel",
        data=excel_buffer,
        file_name="cheque_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<br><br>', unsafe_allow_html=True)  # Add vertical space
