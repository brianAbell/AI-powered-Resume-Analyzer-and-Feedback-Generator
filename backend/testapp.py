import unittest
import json
import sys
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
    def test_file_size_limit_exceeded(self):
        with open("resumes/too_large_file.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')

            response = self.app.post('/process-file',
                                    json={'fileContent': encoded_file},
                                    content_type='application/json')
            
            self.assertEqual(response.status_code, 413)
            self.assertEqual(response.get_json(), {'error': 'File size exceeds the limit.'})


    #test 3: ______________________________________________________
    def test_file_processing_no_text(self):
        # Open pdf, read as bytes
        with open("resumes/no_text_resume.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()

            encoded_file = base64.b64encode(file_bytes).decode('utf-8')

            # Construct a test request data
            test_request_data = json.dumps({'fileContent': encoded_file})

            # Construct a test request context
            with app.test_request_context(data=test_request_data, content_type='application/json', method='POST'):
                # Get the response from the function
                response = process_file()
            
            # Expect empty or very minimal text
            response_data = json.loads(response.data.decode('utf-8'))
            self.assertTrue(len(response_data['extractedText']) < 1)
            self.assertTrue(len(response_data['extractedText']) < 10)
    
    #test 4: _________________________________________________________
    #NOTE: test_client() may be returning 200 and not 413. POSTMAN testing required
    def test_file_processing_very_large(self):
        # Open the too large PDF and read as bytes
        with open("resumes/too_large_file.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()

            encoded_file = base64.b64encode(file_bytes).decode('utf-8')

            # Send this large data to your endpoint
            response = self.app.post('/process-file',
                                    json={'fileContent': encoded_file},
                                    content_type='application/json')
                                
            # Expect a 413 Payload Too Large status code
            self.assertEqual(response.status_code, 413) 
    # _______________________________________________________________

    # GPT4 INTERACTION TESTS ____________________________________________
    # test 1: _______________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_resume_feedback_valid(self, mock_create):
        # Mocking the OpenAI API response
        mock_create.return_value = {
            'choices': [{
                'message': {'content': 'Sample reply for resume-feedback'}
            }]
        }

        response = self.app.post('/resume-feedback',
                                data=json.dumps({'input_text': 'Sample Resume Content'}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'reply': 'Sample reply for resume-feedback'})

    # test 2: __________________________________________________________
    @patch('app.openai.ChatCompletion.create')
    def test_resume_feedback_invalid(self, mock_openai_create):
        # Mocking the OpenAI API call to return a predefined response
        mock_openai_create.return_value = {
            'choices': [
                {'message': {'content': 'Some reply from the mocked API.'}}
            ]
        }
        
        # Sending POST request without 'input' key in JSON
        response = self.app.post('/resume-feedback', json={}, content_type='application/json')
        
        # Check if the API was not called due to invalid input
        mock_openai_create.assert_not_called()
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Input text is required.'})

    # ___________________________________________________________________



            

        

if __name__ == '__main__':
    unittest.main()
