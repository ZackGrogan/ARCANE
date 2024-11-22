from ..ai_services.flux.interface import AIServiceInterface, AIServiceError
import requests
import os
import logging

logger = logging.getLogger(__name__)

class FLUXClient(AIServiceInterface):

    def __init__(self):
        self.api_key = os.getenv('FLUX_API_KEY')
        self.base_url = "https://api.flux.com"

    def generate_profile_picture(self, prompt: str) -> str:
        try:
            response = requests.post(f"{self.base_url}/generate-image", json={'prompt': prompt}, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            # Assuming the API returns a URL to the generated image
            return response.json().get('image_url')
        except Exception as e:
            logger.error(f"FLUX generate_profile_picture error: {e}")
            self.handle_error(e)

    def generate_name(self, prompt: str) -> str:
        raise NotImplementedError("FLUX does not support name generation.")

    def generate_backstory(self, prompt: str) -> str:
        raise NotImplementedError("FLUX does not support backstory generation.")
