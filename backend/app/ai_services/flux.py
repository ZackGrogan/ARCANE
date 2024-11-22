from .interface import AIServiceInterface, AIServiceError
import requests
import os
import logging
from typing import Optional
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class FLUXClient(AIServiceInterface):

    def __init__(self):
        self.api_key = os.getenv('FLUX_API_KEY')
        self.base_url = "https://api.flux.com"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def generate_profile_picture(self, prompt: str, style: Optional[str] = None) -> str:
        try:
            payload = {'prompt': prompt}
            if style:
                payload['style'] = style
            response = requests.post(
                f"{self.base_url}/generate-image",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            image_url = data.get('image_url')
            if not image_url:
                raise AIServiceError("Image URL not found in response")
            return image_url
        except requests.exceptions.RequestException as e:
            logger.error(f"FLUX API request error: {e}")
            raise AIServiceError("Error communicating with FLUX API")
        except ValueError:
            logger.error("Invalid JSON response from FLUX API")
            raise AIServiceError("Invalid response from FLUX API")
        except AIServiceError as e:
            logger.error(f"FLUX API service error: {e}")
            raise

    def generate_name(self, prompt: str) -> str:
        raise NotImplementedError("FLUX does not support name generation.")

    def generate_backstory(self, prompt: str) -> str:
        raise NotImplementedError("FLUX does not support backstory generation.")

    def download_and_process_image(self, image_url: str, save_path: str) -> str:
        """
        Downloads an image from a URL, processes it using Pillow, and saves it locally.

        :param image_url: URL of the image to download
        :param save_path: Path to save the processed image
        :return: Path to the saved image
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGB')  # Convert to RGB if necessary
            image = image.resize((512, 512), Image.LANCZOS)  # Resize to a standard size
            image.save(save_path, format='JPEG', quality=85)  # Save as JPEG with compression
            return save_path
        except Exception as e:
            logger.error(f"Error downloading or processing image: {e}")
            raise AIServiceError("Failed to download or process image")
