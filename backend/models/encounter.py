from typing import List
from .npc import NPC

class Encounter:
    def __init__(self, title: str, description: str, difficulty: str, npcs: List[NPC], monsters: List[str], environment: str, loot: List[str], notes: str):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.npcs = npcs
        self.monsters = monsters
        self.environment = environment
        self.loot = loot
        self.notes = notes

    def calculate_difficulty(self):
        # Example calculation, replace with actual logic
        return len(self.monsters) * 10
