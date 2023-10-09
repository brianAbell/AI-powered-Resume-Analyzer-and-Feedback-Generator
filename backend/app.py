#contains our Flask application code
#NOTE: This code imports the Flask library, 
# creates a new Flask application, 
# defines a single route that returns "Hello, World!" when accessed, 
# and starts the development server when the script is run.
from flask import Flask, request, jsonify
import openai
import os
import PyPDF2
import dotenv
import base64

from io import BytesIO

from dotenv import load_dotenv
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
#new route for GPT API requests
#NOTE: This code defines a new route named /gpt4 that accepts POST requests, 
# reads the input field from the incoming JSON data, 
# calls the GPT-4 API using the OpenAI library, 
# and returns the result as a JSON object.
@app.route('/gpt4', methods=['POST'])
def generate_text():
    input_text = request.json.get('input', '')

    # Generate a response using OpenAI's GPT-4
    response = openai.ChatCompletion.create(
      model="gpt4",  # Replace with the actual model name you're using
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )

    # Extract the assistant's reply from the response
    reply = response['choices'][0]['message']['content']

    # Here we are returning the reply as a JSON response
    return jsonify({'reply': reply})

# send the extracted text as a prompt to the API
@app.route('/get-gpt-response', methods=['POST'])
def get_gpt_response():
    input_text = request.json['input_text']
    response = openai.ChatCompletion.create(
        model="gpt4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )
    reply = response['choices'][0]['message']['content']
    return jsonify({'reply': reply})
# _____________________________________________________________

if __name__ == '__main__':
    app.run(debug=True)