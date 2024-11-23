from typing import List, Tuple, Dict, Any
from flask_pymongo import PyMongo
from .npc import NPC
from .encounter import Encounter

class Campaign:
    def __init__(self, mongo: PyMongo, title: str, description: str, start_date: str, status: str = 'active', notes: str = '', npcs: List[str] = None, encounters: List[str] = None, maps: List[str] = None):
        self.mongo = mongo
        self.title = title
        self.description = description
        self.start_date = start_date
        self.status = status
        self.notes = notes
        self.npcs = npcs if npcs is not None else []
        self.encounters = encounters if encounters is not None else []
        self.maps = maps if maps is not None else []

    def save(self):
        campaign_data = self.__dict__.copy()
        campaign_data.pop('mongo')
        self.mongo.db.campaigns.insert_one(campaign_data)

    def update(self, updates: Dict[str, Any]):
        self.mongo.db.campaigns.update_one({'title': self.title}, {'$set': updates})

    def delete(self):
        self.mongo.db.campaigns.delete_one({'title': self.title})

    @staticmethod
    def get_campaign(mongo: PyMongo, title: str):
        return mongo.db.campaigns.find_one({'title': title})

    @staticmethod
    def list_campaigns(mongo: PyMongo):
        return list(mongo.db.campaigns.find())

    def update_progress(self, completed_encounters: int, total_encounters: int):
        if total_encounters > 0:
            progress = (completed_encounters / total_encounters) * 100
            self.update({'progress': progress})
        else:
            self.update({'progress': 0})

    def add_npc(self, npc_id: str):
        if npc_id not in self.npcs:
            self.npcs.append(npc_id)
            self.update({'npcs': self.npcs})

    def remove_npc(self, npc_id: str):
        if npc_id in self.npcs:
            self.npcs.remove(npc_id)
            self.update({'npcs': self.npcs})

    def add_encounter(self, encounter_id: str):
        if encounter_id not in self.encounters:
            self.encounters.append(encounter_id)
            self.update({'encounters': self.encounters})

    def remove_encounter(self, encounter_id: str):
        if encounter_id in self.encounters:
            self.encounters.remove(encounter_id)
            self.update({'encounters': self.encounters})
