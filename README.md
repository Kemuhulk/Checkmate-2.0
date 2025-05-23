# CheckMate: Automated Bank Check Processor

## Project Overview

CheckMate is an automated solution for processing bank cheques. It extracts relevant details such as payee name, amount, IFSC, account number, and date from scanned cheque images or PDFs using **Gemini API** and **Tesseract OCR**.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/checkmate.git
   cd checkmate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database and configure `config.py` with your **Gemini API** key and **Tesseract** path.

4. Run the Streamlit app:

   ```bash
   streamlit run Home.py
   ```

5. Access the app at `http://localhost:8501`.

## Configuration

Configure `config.py` with your **Gemini API Key** and **Tesseract path**.

## License

MIT License
