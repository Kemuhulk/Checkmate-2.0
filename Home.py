import streamlit as st

st.set_page_config(page_title="CheckMate - Home", page_icon="🏦", layout="wide")

# Title and Introduction
st.title("🏦 CheckMate: Automated Bank Cheque Processor")
st.subheader("Welcome! Choose an option below:")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_📄_Cheque_Processing.py", label="Process a New Cheque", icon="📄")
    st.page_link("pages/3_📈_Analytics.py", label="View Analytics", icon="📈")

with col2:
    st.page_link("pages/2_📊_Cheque_Dashboard.py", label="View Cheque Dashboard", icon="📊")
    st.page_link("pages/4_📂_Export_Data.py", label="Export Cheque Data", icon="📂")

# About CheckMate
st.markdown(
    """
    ---
    **CheckMate** is a tool that extracts and verifies cheque details using AI.  
    - Upload & Extract: Simply upload a scanned cheque, and AI will extract all relevant details.
    - Dashboard Insights: View and track processed cheques efficiently.
    - Export Options: Download cheque data in CSV, JSON, or Excel formats.
    - Analytics & Reports: Gain insights through success rates, bank-wise cheque distribution, and processing trends.
    """
)
