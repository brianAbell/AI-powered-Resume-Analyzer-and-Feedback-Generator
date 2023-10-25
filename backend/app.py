# Following PEP 8 guidelines
import base64
import os
from flask_cors import CORS
from io import BytesIO
import PyPDF2
import openai
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Used to resolve front/back-end communication issues

# INTRO TESTING ______________________________________________
@app.route('/')
def hello_world():
    """
    Basic endpoint to check if the API is up and running.
    :return: A hello world string.
    """
    return 'Hello, World!'


# FILE PROCESSING ____________________________________________
@app.route('/process-file', methods=['POST'])
def process_file():
    """
    Process an uploaded PDF by extracting its text.
    :param: A JSON payload containing a base64 encoded PDF.
    :return: A JSON response with the extracted text or an error message.
    """
    logging.info("Received a request to process a PDF.")
    
    try:
        # Get the base64-encoded file content from the request's JSON payload
        file_data = request.json.get('fileContent', '')

        # Check and strip base64 prefix
        if file_data.startswith("data:application/pdf;base64,"):
            file_data = file_data.split(",")[1]

        logging.info(f"Received file content: {file_data[:100]}...")  # Print the first 100 characters

        # Decode the base64 string to get the binary data
        file_bytes = BytesIO(base64.b64decode(file_data))

        logging.info(f"Decoded file bytes: {file_bytes.getvalue()[:100]}...")  # Print the first 100 bytes
        
        # Extract text from PDF if data is received
        if file_bytes:
            pdf_file = PyPDF2.PdfReader(file_bytes)
            text = ''
            for page in range(len(pdf_file.pages)):
                text += pdf_file.pages[page].extract_text()
            
            logging.info(f"Successfully processed a PDF with {len(pdf_file.pages)} pages.")
            return jsonify({'extractedText': text})
        else:
            return jsonify({'error': 'Invalid file content.'}), 400

    except Exception as e:
        logging.error(f"Error processing file: {e}")

        # Check if the error is a PdfReadError
        if 'EOF marker not found' in str(e):
            return jsonify({'error': 'Invalid or corrupt PDF file.'}), 400
        else:
            return jsonify({'error': 'An error occurred processing the file.'}), 500


# GPT4 INTERACTION ____________________________________________
@app.route('/resume-feedback', methods=['POST'])
def get_resume_feedback():
    """
    Sends the parsed resume to GPT-4 for analysis and returns feedback.
    :param: A JSON payload containing the input text (resume content).
    :return: A JSON response with GPT-4 feedback or an error message.
    """
    input_text = request.json.get('input_text', '')
    if not input_text:
        return jsonify({'error': 'Input text is required.'}), 400

    # Send parsed resume to GPT-4 for analysis
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Provide constructive feedback and suggestions for the following resume:"},
            {"role": "user", "content": input_text},
        ]
    )

    # Extract and return the model's reply
    reply = response['choices'][0]['message']['content']
    logging.info("Successfully obtained feedback from GPT-4 for a resume.")
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)
