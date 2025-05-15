import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def connect_db():
    """Establish connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except psycopg2.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

def create_cheque_table():
    """Creates a table to store cheque images and their extracted data."""
    conn = connect_db()
    if not conn:
        return  

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cheques (
                    id SERIAL PRIMARY KEY,
                    filename TEXT UNIQUE,
                    payee TEXT,
                    amount_words TEXT,
                    amount_digits TEXT,
                    bank TEXT,
                    ifsc_code TEXT,
                    account_number TEXT,
                    cheque_number TEXT,
                    cheque_date TEXT,
                    signature_verification TEXT,
                    status TEXT DEFAULT 'Pending',  -- (Pending, Successful, Failed)
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✅ Cheque table is ready.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error creating table: {e}")
    finally:
        conn.close()

def store_cheque_data(filename, check_data):
    """Stores cheque details and image filename in the database."""
    conn = connect_db()
    if not conn:
        return  

    try:
        with conn.cursor() as cursor:
            # Debugging: Print the received data before inserting
            print("📌 Storing Cheque Data:", check_data)

            query = """
                INSERT INTO cheques (
                    filename, payee, amount_words, amount_digits, bank, ifsc_code,
                    account_number, cheque_number, cheque_date, signature_verification, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                filename,
                check_data.get("Payee Name", "Not Found"),  # If key is missing, stores "Not Found"
                check_data.get("Amount in Words", "Not Found"),
                check_data.get("Amount in Digits", "Not Found"),
                check_data.get("Bank Name", "Not Found"),
                check_data.get("IFSC Code", "Not Found"),
                check_data.get("Account Number", "Not Found"),
                check_data.get("Cheque Number", "Not Found"),
                check_data.get("Date", "Not Found"),
                check_data.get("Signature Verification", "Not Found"),
                check_data.get("Status", "Pending"),  # Default to 'Pending' if key is missing
            )

            cursor.execute(query, values)
            conn.commit()
            print(f"✅ Cheque data for {filename} stored successfully.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error storing cheque data: {e}")
    finally:
        conn.close()

def get_all_cheques():
    """Fetch all cheques from the database."""
    conn = connect_db()
    if not conn:
        return []  

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT cheque_number, amount_digits, cheque_date, status FROM cheques;")
            data = cursor.fetchall()

            return [
                {
                    "Cheque Number": row[0], 
                    "Amount": row[1], 
                    "Date": row[2], 
                    "Status": row[3]
                }
                for row in data
            ]
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return []
    finally:
        conn.close()
