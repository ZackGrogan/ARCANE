from typing import Dict, List

class NPC:
    def __init__(self, name: str, race: str, class_type: str, level: int, background: str, personality: str, abilities: Dict[str, int], skills: List[str], equipment: List[str], description: str, portrait_url: str):
        self.name = name
        self.race = race
        self.class_type = class_type
        self.level = level
        self.background = background
        self.personality = personality
        self.abilities = abilities
        self.skills = skills
        self.equipment = equipment
        self.description = description
        self.portrait_url = portrait_url

    def calculate_attack_bonus(self):
        # Example calculation, replace with actual logic
        return self.level + self.abilities.get('strength', 0)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
