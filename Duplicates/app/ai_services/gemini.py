from ..ai_services.interface import AIServiceInterface, AIServiceError
from ..ai_services.gemini import GoogleGeminiProClient
import requests
import os
import logging

logger = logging.getLogger(__name__)

class GoogleGeminiProClient(AIServiceInterface):

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://api.gemini.com"

    def generate_name(self, prompt: str) -> str:
        template = "Generate a unique fantasy name for a character based on the following description: {}"
        full_prompt = template.format(prompt)
        try:
            response = requests.post(
                f"{self.base_url}/generate-name",
                json={'prompt': full_prompt},
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            response.raise_for_status()
            name = response.json().get('name')
            if not name:
                raise AIServiceError("No name received from Gemini API.")
            return name
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logger.error(f"Gemini Pro generate_name error: {e}")
            self.handle_error(e)

    def generate_backstory(self, prompt: str) -> str:
        template = "Create a detailed backstory for a character with the following traits: {}"
        full_prompt = template.format(prompt)
        try:
            response = requests.post(
                f"{self.base_url}/generate-backstory",
                json={'prompt': full_prompt},
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            response.raise_for_status()
            backstory = response.json().get('backstory')
            if not backstory:
                raise AIServiceError("No backstory received from Gemini API.")
            return backstory
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            logger.error(f"Gemini Pro generate_backstory error: {e}")
            self.handle_error(e)

    def generate_profile_picture(self, prompt: str) -> str:
        raise NotImplementedError("Gemini Pro does not support profile picture generation.")
