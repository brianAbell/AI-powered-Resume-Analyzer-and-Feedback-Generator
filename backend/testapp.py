import unittest
import json
import sys
import PyPDF2
import base64
from app import app  # Importing the Flask app
from app import process_file
from flask import Flask
from unittest.mock import patch

#TODO: transition to pytest for simpler syntax
class AppTestCase(unittest.TestCase):
    # called before every individual test, sets up vars
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 
    
    # INTRO TESTS ______________________________________________
    # test 1: _____________________________________________________
    def test_home_status_code(self):
        # Sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # Asserts the status code of HTTP Response
        self.assertEqual(result.status_code, 200)  

    #test 2: ______________________________________________________
    def test_get_hello_world(self):
        # Sends HTTP GET request to the application
        # to check if "Hello, World!" is displayed
        result = self.app.get('/')

        self.assertEqual(result.data, b'Hello, World!')
    # ____________________________________________________________
    
    # FILE PROCESSING TESTS ____________________________________________
    #test 1: ______________________________________________________
    def test_file_processing_valid(self):
        # Open pdf, read as bytes
        with open("resumes/resume.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()

            encoded_file = base64.b64encode(file_bytes).decode('utf-8')

            # Construct a test request data (as it would come from the client)
            test_request_data = json.dumps({'fileContent': encoded_file})
            
            # Construct a test request context
            with app.test_request_context(data=test_request_data, content_type='application/json', method='POST'):
                # Get the response from the function
                response = process_file()
            
            # Validate the response... e.g., check status code, check if extractedText in response data, etc.
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertIn('extractedText', response_data)
            self.assertIsInstance(response_data['extractedText'], str)
            #... any other assertions based on your function's expected behavior
    
    #test 2: ______________________________________________________
    def test_file_processing_invalid(self):
        invalid_input = "not_a_base64_encoded_pdf"

        response = self.app.post('/process-file',
                                 json={'fileContent': invalid_input},
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Invalid or corrupt PDF file.'})
    # _______________________________________________________________

    # GPT4 INTERACTION TESTS ____________________________________________
    #NOTE: using unittest's 'mock' to avoid actual API calls
    # test 1: ______________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_generate_text_valid(self, mock_create):
        mock_create.return_value = {
            'choices': [{
                'message': {'content': 'Sample reply for gpt4'}
            }]
        }

        response = self.app.post('/gpt4',
                                 data=json.dumps({'input': 'Hello, GPT!'}),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'reply': 'Sample reply for gpt4'})
        

    # test 2: ______________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_get_gpt_response_valid(self, mock_create):
        # Mocking the OpenAI API response
        mock_create.return_value = {
            'choices': [{
                'message': {'content': 'Sample reply for get-gpt-response'}
            }]
        }
        
        response = self.app.post('/get-gpt-response',
                                 data=json.dumps({'input_text': 'Hello again, GPT!'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'reply': 'Sample reply for get-gpt-response'})
        
    # test 3: ______________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_generate_text_invalid(self, mock_openai_create):
        # Mocking the OpenAI API call to return a predefined response
        mock_openai_create.return_value = {
            'choices': [
                {'message': {'content': 'Some reply from the mocked API.'}}
            ]
        }
        
        # Sending POST request without 'input' key in JSON
        response = self.app.post('/gpt4', json={}, content_type='application/json')
        
        # Check if the API was not called due to invalid input
        mock_openai_create.assert_not_called()
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Input text is required.'})

    # test 4: ______________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_get_gpt_response_invalid(self, mock_openai_create):
        # Mocking the OpenAI API call to return a predefined response
        mock_openai_create.return_value = {
            'choices': [
                {'message': {'content': 'Some reply from the mocked API.'}}
            ]
        }

        # Sending POST request without 'input_text' key in JSON
        response = self.app.post('/get-gpt-response', json={}, content_type='application/json')
        
        # Check if the API was not called due to invalid input
        mock_openai_create.assert_not_called()
        
        # Check for a 400 error and an appropriate error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Input text is required.'})
    # ___________________________________________________________________



            

        

if __name__ == '__main__':
    unittest.main()
