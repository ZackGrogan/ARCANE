from typing import List, Tuple
from .npc import NPC
from .encounter import Encounter

class Campaign:
    def __init__(self, title: str, description: str, setting: str, level_range: Tuple[int, int], encounters: List[Encounter], npcs: List[NPC], maps: List[str], notes: str):
        self.title = title
        self.description = description
        self.setting = setting
        self.level_range = level_range
        self.encounters = encounters
        self.npcs = npcs
        self.maps = maps
        self.notes = notes

    def update_progress(self, progress):
        # Example logic, replace with actual logic
        pass
