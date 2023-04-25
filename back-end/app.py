#contains our Flask application code
#NOTE: This code imports the Flask library, 
# creates a new Flask application, 
# defines a single route that returns "Hello, World!" when accessed, 
# and starts the development server when the script is run.
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#new route for GPT API requests
#NOTE: This code defines a new route named /gpt4 that accepts POST requests, 
# reads the input field from the incoming JSON data, 
# calls the GPT-3 API using the OpenAI library, 
# and returns the result as a JSON object.
@app.route('/gpt4', methods=['POST'])
def gpt4():
    input_text = request.json.get('input', '')

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return jsonify({'output': response.choices[0].text})

if __name__ == '__main__':
    app.run(debug=True)