from typing import List, Dict
from .npc import NPC
from backend.app.utils.dnd_api_client import DnDApiClient
from flask_pymongo import PyMongo

class Encounter:
    def __init__(self, mongo: PyMongo, title: str, description: str, difficulty: str, npcs: List[NPC], monsters: List[str], environment: str, loot: List[str], notes: str, monster_data: List[Dict] = None):
        self.mongo = mongo
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.npcs = npcs
        self.monsters = monsters
        self.environment = environment
        self.loot = loot
        self.notes = notes
        self.monster_data = monster_data if monster_data is not None else []

    def save(self):
        self.mongo.db.encounters.insert_one(self.__dict__)

    def calculate_difficulty(self):
        # Example calculation, replace with actual logic
        return len(self.monsters) * 10

    def add_monster(self, monster_name: str):
        client = DnDApiClient()
        monster_data = client.get_monster(monster_name)
        if monster_data:
            self.monster_data.append(monster_data)
