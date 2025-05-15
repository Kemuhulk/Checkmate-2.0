import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
import os

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Page Configuration
st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")
# Function to fetch data from PostgreSQL
def fetch_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Fetch cheque processing data
        query = """
        SELECT bank, COUNT(*) AS cheque_count 
        FROM cheques
        GROUP BY bank
        ORDER BY cheque_count DESC;
        """
        df = pd.read_sql(query, conn)

        # Fetch success & failure count
        query_success = "SELECT COUNT(*) FROM cheques WHERE status='successful';"
        cursor.execute(query_success)
        successful_cheques = cursor.fetchone()[0]

        query_unsuccessful = "SELECT COUNT(*) FROM cheques WHERE status='failed';"
        cursor.execute(query_unsuccessful)
        unsuccessful_cheques = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        total_cheques = successful_cheques + unsuccessful_cheques
        success_rate = (successful_cheques / total_cheques) * 100 if total_cheques > 0 else 0

        return df, total_cheques, successful_cheques, unsuccessful_cheques, success_rate

    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame(), 0, 0, 0, 0

# Fetch data
df, total_cheques, successful_cheques, unsuccessful_cheques, success_rate = fetch_data()

# Header
st.markdown("<h1 style='text-align: center; color: white;'>📊 Analytics</h1>", unsafe_allow_html=True)

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Cheques Processed", total_cheques)
col2.metric("Successful Cheques", successful_cheques)
col3.metric("Unsuccessful Cheques", unsuccessful_cheques)

st.markdown("---")
# Success Rate
st.markdown("### Cheque Processing Success Rate")
st.write(f"**Success Rate:** {success_rate:.2f}%")

# Success Rate Over Time (Modify query based on actual date field)
query_time_series = """
SELECT DATE(processed_at) AS date, 
       (SUM(CASE WHEN status = 'successful' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS success_rate
FROM cheques
GROUP BY date
ORDER BY date;
"""

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    success_data = pd.read_sql(query_time_series, conn)
    conn.close()

    if not success_data.empty:
        fig_line = px.line(success_data, x="date", y="success_rate", title="Success Rate Over Time",
                           line_shape="linear", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("No success rate data available.")
except Exception as e:
    st.error(f"Failed to load time series data: {e}")

st.markdown("---")
# Cheque Distribution by Bank
st.markdown("### Cheque Distribution by Bank")
if not df.empty:
    fig_bar = px.bar(df, x="bank", y="cheque_count", text="cheque_count",
                     title="Cheque Distribution by Bank",
                     color_discrete_sequence=["#1F77B4"])
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("No cheque data available.")
