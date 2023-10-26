import unittest
import json
import base64
from app import app, process_file
from flask import Flask
from unittest.mock import patch

# TODO: transition to pytest for simpler syntax


class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        """Initialize test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    # Intro tests
    def test_home_status_code(self):
        """Test status code for the home route."""
        result = self.app.get('/')  # Making a GET request to the home route
        self.assertEqual(result.status_code, 200)

    def test_get_hello_world(self):
        """Test if 'Hello, World!' is displayed for the home route."""
        result = self.app.get('/')
        self.assertEqual(result.data, b'Hello, World!')

    # File processing tests
    def test_file_processing_valid(self):
        """Test valid file processing."""
        # Reading and encoding the sample PDF
        with open("resumes/resume.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
            test_request_data = json.dumps({'fileContent': encoded_file})

        # Sending the encoded file to the processing endpoint
        with app.test_request_context(data=test_request_data, content_type='application/json', method='POST'):
            response = process_file()

        # Checking the response for expected behavior
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertIn('extractedText', response_data)
        self.assertIsInstance(response_data['extractedText'], str)

    def test_file_size_limit_exceeded(self):
        """Test for exceeding the file size limit."""
        # Reading and encoding a large file
        with open("resumes/too_large_file.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
            
        # Sending the encoded file to the processing endpoint
        response = self.app.post('/process-file', json={'fileContent': encoded_file}, content_type='application/json')
        
        # Checking for expected error response
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json(), {'error': 'File size exceeds the limit.'})

    def test_file_processing_no_text(self):
        """Test file processing with no text."""
        # Reading and encoding a file with minimal text
        with open("resumes/no_text_resume.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
            test_request_data = json.dumps({'fileContent': encoded_file})

        # Sending the encoded file to the processing endpoint
        with app.test_request_context(data=test_request_data, content_type='application/json', method='POST'):
            response = process_file()

        # Checking for expected behavior (minimal text in response)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(response_data['extractedText']) < 10)

    def test_file_processing_very_large(self):
        """Test file processing with very large files. Expect a 413 status code."""
        # Reading and encoding a very large file
        with open("resumes/too_large_file.pdf", "rb") as pdf_file:
            file_bytes = pdf_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')
            
        # Sending the encoded file to the processing endpoint
        response = self.app.post('/process-file', json={'fileContent': encoded_file}, content_type='application/json')
        
        # Expecting a 'Payload Too Large' response
        self.assertEqual(response.status_code, 413)

    # GPT-4 interaction tests
    @patch('app.openai.ChatCompletion.create')
    def test_resume_feedback_valid(self, mock_create):
        """Test valid resume feedback."""
        # Mocking the OpenAI API response
        mock_create.return_value = {'choices': [{'message': {'content': 'Sample reply for resume-feedback'}}]}
        
        # Sending a sample resume text for feedback
        response = self.app.post('/resume-feedback', data=json.dumps({'input_text': 'Sample Resume Content'}), content_type='application/json')
        
        # Checking for expected response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'reply': 'Sample reply for resume-feedback'})

    @patch('app.openai.ChatCompletion.create')
    def test_resume_feedback_invalid(self, mock_openai_create):
        """Test invalid resume feedback. Expect a 400 status code."""
        # Mocking the OpenAI API call
        mock_openai_create.return_value = {'choices': [{'message': {'content': 'Some reply from the mocked API.'}}]}
        
        # Sending an invalid request
        response = self.app.post('/resume-feedback', json={}, content_type='application/json')
        
        # Checking for expected error response
        mock_openai_create.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Input text is required.'})


if __name__ == '__main__':
    unittest.main()
