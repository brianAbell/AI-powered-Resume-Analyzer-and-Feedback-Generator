# Following PEP 8 guidelines
import base64
import os

from io import BytesIO
import PyPDF2
import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")


app = Flask(__name__)

# INTRO TESTING ______________________________________________
@app.route('/')
def hello_world():
    return 'Hello, World!'
# ____________________________________________________________

# FILE PROCESSING ____________________________________________
# NOTE: endpoint accepts a POST req w base64 encoded PDF.
# NOTE: then decodes file, extract text using PyPDF2, returns text
@app.route('/process-file', methods=['POST'])
def process_file():
    try:
        # Get the base64-encoded file content from the request's JSON payload
        file_data = request.json.get('fileContent', '')

        # Decode the base64 string to get the binary data
        file_bytes = BytesIO(base64.b64decode(file_data))
        
        # If we received some data
        if file_bytes:
            # Create a PDF file reader object
            pdf_file = PyPDF2.PdfReader(file_bytes)

            # Initialize an empty string to store the extracted text
            text = ''

            # Loop over all the pages in the PDF file
            for page in range(len(pdf_file.pages)):
                # Extract the text from the current page and append it to our text string
                text += pdf_file.pages[page].extract_text()
            
            # Return the extracted text in a JSON response
            return jsonify({'extractedText': text})
        
        # If we didn't receive any data, return an error message
        else:
            return jsonify({'error': 'Invalid file content.'}), 400
    except Exception as e:
        # Check if the error is a PdfReadError
        if 'EOF marker not found' in str(e):
            return jsonify({'error': 'Invalid or corrupt PDF file.'}), 400
        # You may add more conditions here to handle different errors differently
        # Else, return a general server error
        else:
            return jsonify({'error': 'An error occurred processing the file.'}), 500
# ____________________________________________________________

# GPT4 INTERACTION ____________________________________________
@app.route('/resume-feedback', methods=['POST'])
def get_resume_feedback():
    # Extract the resume text
    input_text = request.json.get('input', '')
    if not input_text:
        return jsonify({'error': 'Input text is required.'}), 400

    # Send parsed resume AND instructions to GPT-4 for analysis
    response = openai.ChatCompletion.create(
        model="gpt4",
        messages=[
            {"role": "system", "content": "Provide constructive feedback and suggestions for the following resume:"},
            {"role": "user", "content": input_text},
        ]
    )

    # Extract and return the model's reply
    reply = response['choices'][0]['message']['content']
    return jsonify({'reply': reply})
# _____________________________________________________________

if __name__ == '__main__':
    app.run(debug=True)