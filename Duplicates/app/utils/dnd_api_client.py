import requests
from functools import lru_cache
import logging
import retrying

logger = logging.getLogger(__name__)

class ApiError(Exception):
    pass

class DnDApiClient:
    BASE_URL = "https://www.dnd5eapi.co/api/"

    def __init__(self):
        logger.info('DnDApiClient initialized')

    @lru_cache(maxsize=128)
    @retrying.retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def get_monster(self, monster_name):
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
    def get_spell(self, spell_name):
        url = f"{self.BASE_URL}spells/{spell_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            raise ApiError(f"Error fetching spell: {spell_name}")

    @lru_cache(maxsize=128)
    @retrying.retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def get_equipment(self, equipment_name):
        url = f"{self.BASE_URL}equipment/{equipment_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            raise ApiError(f"Error fetching equipment: {equipment_name}")
