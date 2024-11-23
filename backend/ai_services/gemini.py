"""Google Gemini Pro AI service client.

This module provides a client for interacting with the Google Gemini Pro API,
implementing the AIServiceInterface for generating character names and backstories.
"""

from ..ai_services.interface import AIServiceInterface, AIServiceError
from ..ai_services.gemini import GoogleGeminiProClient
import requests
import os
import logging

logger = logging.getLogger(__name__)

class GoogleGeminiProClient(AIServiceInterface):
    """Client for interacting with the Google Gemini Pro API.

    This class implements the AIServiceInterface to provide AI-powered
    character name and backstory generation services.

    Attributes:
        api_key (str): Google Gemini Pro API key from environment variables
        base_url (str): Base URL for the Gemini API
    """

    def __init__(self):
        """Initialize the Gemini Pro client.

        The API key is retrieved from the GEMINI_API_KEY environment variable.
        """
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://api.gemini.com"

    def generate_name(self, prompt: str) -> str:
        """Generate a character name using Gemini Pro.

        Args:
            prompt (str): Description or context for name generation

        Returns:
            str: Generated character name

        Raises:
            AIServiceError: If the API request fails or returns invalid data
        """
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
        """Generate a character backstory using Gemini Pro.

        Args:
            prompt (str): Character traits and context for backstory generation

        Returns:
            str: Generated character backstory

        Raises:
            AIServiceError: If the API request fails or returns invalid data
        """
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
        """Generate a character profile picture using Gemini Pro.

        Args:
            prompt (str): Description or context for profile picture generation

        Returns:
            str: Generated character profile picture

        Raises:
            NotImplementedError: Gemini Pro does not support profile picture generation
        """
        raise NotImplementedError("Gemini Pro does not support profile picture generation.")

    def handle_error(self, error: Exception) -> None:
        """Handle API errors by raising appropriate exceptions.

        Args:
            error (Exception): The original error that occurred

        Raises:
            AIServiceError: Wrapped error with appropriate message
        """
        raise AIServiceError("An error occurred while using the Gemini Pro API") from error
