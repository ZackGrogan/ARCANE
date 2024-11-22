from typing import Dict, List
from backend.app.utils.dnd_api_client import DnDApiClient

class NPC:
    def __init__(self, name: str, race: str, class_type: str, level: int, background: str, personality: str, abilities: Dict[str, int], skills: List[str], equipment: List[str], description: str, portrait_url: str, spells: List[Dict] = None, equipment_data: List[Dict] = None):
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
        self.spells = spells if spells is not None else []
        self.equipment_data = equipment_data if equipment_data is not None else []

    def calculate_attack_bonus(self):
        # Example calculation, replace with actual logic
        return self.level + self.abilities.get('strength', 0)

    def add_spell(self, spell_name: str):
        client = DnDApiClient()
        spell_data = client.get_spell(spell_name)
        if spell_data:
            self.spells.append(spell_data)

    def add_equipment(self, equipment_name: str):
        client = DnDApiClient()
        equipment_data = client.get_equipment(equipment_name)
        if equipment_data:
            self.equipment_data.append(equipment_data)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
