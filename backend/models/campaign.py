from typing import List, Tuple
from flask_pymongo import PyMongo
from .npc import NPC
from .encounter import Encounter

class Campaign:
    def __init__(self, mongo: PyMongo, title: str, description: str, setting: str, level_range: Tuple[int, int], encounters: List[Encounter], npcs: List[NPC], maps: List[str], notes: str):
        self.mongo = mongo
        self.title = title
        self.description = description
        self.setting = setting
        self.level_range = level_range
        self.encounters = encounters
        self.npcs = npcs
        self.maps = maps
        self.notes = notes

    def save(self):
        self.mongo.db.campaigns.insert_one(self.__dict__)

    def update_progress(self, progress):
        # Example logic, replace with actual logic
        pass
