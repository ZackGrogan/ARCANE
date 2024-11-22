from .interface import AIServiceInterface, AIServiceError
import requests
import os
import logging

logger = logging.getLogger(__name__)

class GoogleGeminiProClient(AIServiceInterface):

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://api.gemini.com"

    def generate_name(self, prompt: str) -> str:
        try:
            response = requests.post(f"{self.base_url}/generate-name", json={'prompt': prompt}, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            return response.json().get('name')
        except Exception as e:
            logger.error(f"Gemini Pro generate_name error: {e}")
            self.handle_error(e)

    def generate_backstory(self, prompt: str) -> str:
        try:
            response = requests.post(f"{self.base_url}/generate-backstory", json={'prompt': prompt}, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            return response.json().get('backstory')
        except Exception as e:
            logger.error(f"Gemini Pro generate_backstory error: {e}")
            self.handle_error(e)

    def generate_profile_picture(self, prompt: str) -> str:
        raise NotImplementedError("Gemini Pro does not support profile picture generation.")
