import os
import requests
from backend.app.ai_services.interface import AIServiceInterface

class GeminiAPIError(Exception):
    pass

class GeminiService(AIServiceInterface):
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.base_url = 'https://api.gemini.com/v1/'

    def generate_name(self, prompt):
        try:
            response = requests.post(
                f'{self.base_url}generate/name',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'prompt': prompt}
            )
            response.raise_for_status()
            return response.json().get('name')
        except requests.RequestException as e:
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
