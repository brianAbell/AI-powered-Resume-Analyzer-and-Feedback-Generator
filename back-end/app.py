#contains our Flask application code
#NOTE: This code imports the Flask library, 
# creates a new Flask application, 
# defines a single route that returns "Hello, World!" when accessed, 
# and starts the development server when the script is run.
from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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

if __name__ == '__main__':
    app.run(debug=True)