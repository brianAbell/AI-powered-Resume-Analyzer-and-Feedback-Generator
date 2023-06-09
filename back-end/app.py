#contains our Flask application code
#NOTE: This code imports the Flask library, 
# creates a new Flask application, 
# defines a single route that returns "Hello, World!" when accessed, 
# and starts the development server when the script is run.
from flask import Flask, request, jsonify
import openai
import os
import PyPDF2
from io import BytesIO

openai.api_key = os.environ.get("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process-file', methods=['POST'])
def process_file():
    # Get the base64-encoded file content from the request's JSON payload
    file_data = request.json.get('fileContent', '')

    # Decode the base64 string to get the binary data
    file_bytes = BytesIO(base64.b64decode(file_data))
    
    # If we received some data
    if file_bytes:
        # Create a PDF file reader object
        pdf_file = PyPDF2.PdfFileReader(file_bytes)

        # Initialize an empty string to store the extracted text
        text = ''

        # Loop over all the pages in the PDF file
        for page in range(pdf_file.getNumPages()):
            # Extract the text from the current page and append it to our text string
            text += pdf_file.getPage(page).extractText()
        
        # Return the extracted text in a JSON response
        return jsonify({'extractedText': text})
    
    # If we didn't receive any data, return an error message
    else:
        return jsonify({'error': 'Invalid file content.'}), 400



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

if __name__ == '__main__':
    app.run(debug=True)