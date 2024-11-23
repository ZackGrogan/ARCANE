import os
import requests
import logging
from backend.app.ai_services.interface import AIServiceInterface

# Configure logger for this module
logger = logging.getLogger(__name__)

class FluxAPIError(Exception):
    pass

class FLUXService(AIServiceInterface):
    def __init__(self):
        self.api_key = os.environ.get('FLUX_API_KEY')
        self.base_url = 'https://api.flux.com/v1/'
        logger.info('FLUXService initialized with base URL: %s', self.base_url)

    def generate_profile_picture(self, prompt):
        try:
            logger.info('Generating profile picture with prompt: %s', prompt)
            response = requests.post(
                f'{self.base_url}generate/profile_picture',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'prompt': prompt}
            )
            response.raise_for_status()
            logger.info('Received response: %s', response.json())
            return response.json().get('image_url')
        except requests.RequestException as e:
            logger.error('Error generating profile picture: %s', e)
            self.handle_error(e)
            return None

    def handle_error(self, error):
        raise FluxAPIError(f"Flux API request failed: {error}")
