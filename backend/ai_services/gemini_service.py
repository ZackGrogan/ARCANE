import os
import requests
import logging
from backend.ai_services.interface import AIServiceInterface

# Configure logger for this module
logger = logging.getLogger(__name__)

class GeminiAPIError(Exception):
    pass

class GeminiService(AIServiceInterface):
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.base_url = 'https://api.gemini.com/v1/'
        logger.info('GeminiService initialized with base URL: %s', self.base_url)

    def generate_name(self, prompt):
        try:
            logger.info('Generating name with prompt: %s', prompt)
            response = requests.post(
                f'{self.base_url}generate/name',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'prompt': prompt}
            )
            response.raise_for_status()
            logger.info('Received response: %s', response.json())
            return response.json().get('name')
        except requests.RequestException as e:
            logger.error('Error generating name: %s', e)
            self.handle_error(e)
            return None

    def generate_backstory(self, prompt):
        try:
            response = requests.post(
                f'{self.base_url}generate/backstory',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'prompt': prompt}
            )
            response.raise_for_status()
            return response.json().get('backstory')
        except requests.RequestException as e:
            self.handle_error(e)
            return None

    def handle_error(self, error):
        raise GeminiAPIError(f"Gemini API request failed: {error}")
