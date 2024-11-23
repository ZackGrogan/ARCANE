from typing import List, Dict, Any
from .npc import NPC
from backend.app.utils.dnd_api_client import DnDApiClient
from flask_pymongo import PyMongo

class Encounter:
    def __init__(self, mongo: PyMongo, title: str, environment: str, party_level: int, difficulty: str, monsters: List[str] = None, traps: List[str] = None, notes: str = ''):
        self.mongo = mongo
        self.title = title
        self.environment = environment
        self.party_level = party_level
        self.difficulty = difficulty
        self.monsters = monsters if monsters is not None else []
        self.traps = traps if traps is not None else []
        self.notes = notes

    def save(self):
        encounter_data = self.__dict__.copy()
        encounter_data.pop('mongo')
        self.mongo.db.encounters.insert_one(encounter_data)

    def update(self, updates: Dict[str, Any]):
        self.mongo.db.encounters.update_one({'title': self.title}, {'$set': updates})

    def delete(self):
        self.mongo.db.encounters.delete_one({'title': self.title})

    @staticmethod
    def get_encounter(mongo: PyMongo, title: str):
        return mongo.db.encounters.find_one({'title': title})

    @staticmethod
    def list_encounters(mongo: PyMongo):
        return list(mongo.db.encounters.find())

    def calculate_difficulty(self):
        # Example calculation, replace with actual logic
        return len(self.monsters) * 10

    def add_monster(self, monster_name: str):
        client = DnDApiClient()
        monster_data = client.get_monster(monster_name)
        if monster_data:
            self.monster_data.append(monster_data)
