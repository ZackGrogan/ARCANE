import os
import http.client
from dotenv import load_dotenv
import unittest
from unittest.mock import patch

# Load the .env file
load_dotenv()

class TestGeminiAPI(unittest.TestCase):
    @patch('http.client.HTTPSConnection')
    def test_generate_content(self, mock_conn):
        mock_conn.return_value.getresponse.return_value.status = 200
        mock_conn.return_value.getresponse.return_value.read.return_value.decode.return_value = '{"text": "AI works by using machine learning algorithms to process and generate human-like text"}'

        if not os.getenv('GEMINI_API_KEY'):
            self.fail("API key not found. Please ensure the GEMINI_API_KEY is set in the .env file.")

        conn = http.client.HTTPSConnection("api.gemini.com")
        headers = {'Authorization': f'Bearer {os.getenv("GEMINI_API_KEY")}', 'Content-Type': 'application/json'}
        conn.request("POST", "/generate-content", '{"prompt": "Explain how AI works"}', headers)
        response = conn.getresponse()

        self.assertEqual(response.status, 200)
        response_data = response.read().decode('utf-8')
        self.assertIn('text', response_data)

if __name__ == '__main__':
    unittest.main()
