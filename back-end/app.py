#contains our Flask application code
#NOTE: This code imports the Flask library, 
# creates a new Flask application, 
# defines a single route that returns "Hello, World!" when accessed, 
# and starts the development server when the script is run.
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)