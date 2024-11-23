"""DnD 5e API client for fetching game data.

This module provides a client for interacting with the DnD 5e API,
offering methods to fetch monsters, spells, and equipment data.
The client includes caching and retry mechanisms for improved performance
and reliability.
"""

import requests
from functools import lru_cache
import logging
import retrying

logger = logging.getLogger(__name__)

class ApiError(Exception):
    """Custom exception for DnD 5e API errors.

    This exception is raised when API requests fail or return unexpected data.
    """
    pass

class DnDApiClient:
    """Client for interacting with the DnD 5e API.

    This class provides methods to fetch various game data from the
    DnD 5e API, including monsters, spells, and equipment. It includes
    caching and retry mechanisms for improved performance and reliability.

    Attributes:
        BASE_URL (str): Base URL for the DnD 5e API
    """

    BASE_URL = "https://www.dnd5eapi.co/api/"

    def __init__(self):
        """Initialize the DnD API client.

        Sets up logging and initializes the client with the base URL.
        """
        logger.info('DnDApiClient initialized')

    @lru_cache(maxsize=128)
    @retrying.retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def get_monster(self, monster_name: str) -> dict:
        """Fetch monster data from the DnD 5e API.

        This method is cached and will retry up to 3 times with exponential backoff.

        Args:
            monster_name (str): Name of the monster to fetch

        Returns:
            dict: Monster data including stats, abilities, and description

        Raises:
            ApiError: If the API request fails or returns invalid data
        """
        logger.info('Fetching monster data for: %s', monster_name)
        url = f"{self.BASE_URL}monsters/{monster_name}"
        response = requests.get(url)
        if response.status_code == 200:
            logger.info('Received monster data: %s', response.json())
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            raise ApiError(f"Error fetching monster: {monster_name}")

    @lru_cache(maxsize=128)
    @retrying.retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def get_spell(self, spell_name: str) -> dict:
        """Fetch spell data from the DnD 5e API.

        This method is cached and will retry up to 3 times with exponential backoff.

        Args:
            spell_name (str): Name of the spell to fetch

        Returns:
            dict: Spell data including level, school, and description

        Raises:
            ApiError: If the API request fails or returns invalid data
        """
        url = f"{self.BASE_URL}spells/{spell_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            raise ApiError(f"Error fetching spell: {spell_name}")

    @lru_cache(maxsize=128)
    @retrying.retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def get_equipment(self, equipment_name: str) -> dict:
        """Fetch equipment data from the DnD 5e API.

        This method is cached and will retry up to 3 times with exponential backoff.

        Args:
            equipment_name (str): Name of the equipment to fetch

        Returns:
            dict: Equipment data including cost, weight, and properties

        Raises:
            ApiError: If the API request fails or returns invalid data
        """
        url = f"{self.BASE_URL}equipment/{equipment_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            raise ApiError(f"Error fetching equipment: {equipment_name}")
