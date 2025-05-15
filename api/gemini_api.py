import google.generativeai as genai
from config import GEMINI_API_KEY
import json
from PIL import Image
import io

genai.configure(api_key=GEMINI_API_KEY)

def analyze_check_with_gemini(image_path=None, image_data=None):
    """
    Sends an image of a cheque to Gemini Pro Vision for direct analysis.
    """

    try:
        if image_path:
            image = Image.open(image_path)  # Convert to PIL.Image
        elif image_data:
            image = Image.open(io.BytesIO(image_data))  # Convert byte data to PIL.Image
        else:
            return {"error": "No valid image input provided."}

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = """
        You are an AI specialized in analyzing bank cheques. Analyze the cheque in this image and extract:

        - Payee Name
        - Amount in Words
        - Amount in Digits
        - Bank Name (Located at the top near the bank logo)
        - IFSC Code (Below the bank name, format: XXXX000YYYY)
        - Account Number (Near "A/C No." or "Account Number")
        - Cheque Number (Found at the bottom of the cheque)
        - Date (At the top-right, format: DD/MM/YYYY)
        - Signature Verification (Bottom-right; return "Present" if detected, otherwise "Absent")
        - Status (successful, unsuccessful, pending)

        **Important Notes:**
        - Return only JSON data, with no explanations.
        - If a value is missing, return `"Not Found"`.
        """

        # Send image directly instead of encoding to base64
        response = model.generate_content([image, {"text": prompt}])

        print("Gemini Raw Response:", response.text)  # Debugging output

        if response.text:
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json") or cleaned_response.startswith("```JSON"):
                cleaned_response = cleaned_response[7:].strip()
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3].strip()

            try:
                return json.loads(cleaned_response)  # Return Gemini's extracted JSON
            except json.JSONDecodeError as e:
                return {"error": f"Gemini returned an invalid JSON response. JSON Error: {str(e)}", "raw_response": cleaned_response}

        return {"error": "No valid response from Gemini API."}

    except Exception as e:
        return {"error": f"Gemini API error: {str(e)}"}
