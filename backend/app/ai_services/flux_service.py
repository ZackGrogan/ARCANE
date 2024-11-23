import os
import requests
from backend.app.ai_services.interface import AIServiceInterface

class FluxAPIError(Exception):
    pass

class FLUXService(AIServiceInterface):
    def __init__(self):
        self.api_key = os.environ.get('FLUX_API_KEY')
        self.base_url = 'https://api.flux.com/v1/'

    def generate_profile_picture(self, prompt):
        try:
            response = requests.post(
                f'{self.base_url}generate/profile_picture',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'prompt': prompt}
            )
            response.raise_for_status()
            return response.json().get('image_url')
        except requests.RequestException as e:
            self.handle_error(e)
            return None

    def handle_error(self, error):
        raise FluxAPIError(f"Flux API request failed: {error}")
