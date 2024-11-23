import logging
from typing import Dict, List, Any
from bson import ObjectId

# Configure logger for this module
logger = logging.getLogger(__name__)

class NPC:
    def __init__(self, mongo, name, race, npc_class=None, class_type=None, level=1, **kwargs):
        """Initialize an NPC.

        Args:
            mongo: MongoDB instance
            name: NPC name
            race: NPC race
            npc_class: NPC class (new parameter name)
            class_type: NPC class (old parameter name for backward compatibility)
            level: NPC level (default: 1)
            **kwargs: Additional fields like background, personality, etc.
        """
        self.mongo = mongo
        self.name = self._validate_name(name)
        self.race = race
        self.npc_class = npc_class or class_type  # Use either npc_class or class_type
        self.level = self._validate_level(level)
        self.background = kwargs.get('background', '')
        self.personality = kwargs.get('personality', '')
        self.abilities = self._validate_abilities(kwargs.get('abilities', {}))
        self.skills = kwargs.get('skills', [])
        self.equipment = kwargs.get('equipment', [])
        self.spells = kwargs.get('spells', [])
        self.description = kwargs.get('description', '')
        self.portrait_url = kwargs.get('portrait_url', '')
        self._id = kwargs.get('_id', None)

    def _validate_name(self, name):
        """Validate NPC name."""
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 100:  # Add reasonable length limit
            raise ValueError("Name is too long (max 100 characters)")
        # Only check for duplicates when saving a new NPC
        if not hasattr(self, '_id') and self.mongo.db.npcs.find_one({'name': name}):
            raise ValueError("An NPC with this name already exists")
        return name

    def _validate_level(self, level):
        """Validate NPC level."""
        try:
            level = int(level)
            if not 1 <= level <= 20:
                raise ValueError("Level must be between 1 and 20")
            return level
        except (TypeError, ValueError):
            raise ValueError("Level must be a number between 1 and 20")

    def _validate_abilities(self, abilities):
        """Validate ability scores."""
        valid_abilities = {'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'}
        if not isinstance(abilities, dict):
            raise ValueError("Abilities must be a dictionary")

        # Convert all ability scores to integers and validate range
        validated = {}
        for ability in valid_abilities:
            score = abilities.get(ability, 10)  # Default to 10 if not provided
            try:
                score = int(score)
                if not 1 <= score <= 30:
                    raise ValueError(f"{ability.capitalize()} score must be between 1 and 30")
                validated[ability] = score
            except (TypeError, ValueError):
                raise ValueError(f"{ability.capitalize()} score must be a number between 1 and 30")
        return validated

    def calculate_modifiers(self):
        """Calculate ability modifiers."""
        return {ability: (score - 10) // 2 for ability, score in self.abilities.items()}

    def add_equipment(self, equipment_name: str) -> None:
        """Add equipment to NPC's inventory.

        Args:
            equipment_name (str): Name of equipment to add
        """
        if not equipment_name:
            raise ValueError("Equipment name cannot be empty")

        # Get equipment data from D&D API
        client = DnDApiClient()
        equipment_data = client.get_equipment(equipment_name)

        if not equipment_data:
            raise ValueError(f"Equipment '{equipment_name}' not found")

        if equipment_name not in self.equipment:
            self.equipment.append(equipment_name)
            self.save()

    def add_spell(self, spell_name: str) -> None:
        """Add spell to NPC's spellbook.

        Args:
            spell_name (str): Name of spell to add
        """
        if not spell_name:
            raise ValueError("Spell name cannot be empty")

        # Get spell data from D&D API
        client = DnDApiClient()
        spell_data = client.get_spell(spell_name)

        if not spell_data:
            raise ValueError(f"Spell '{spell_name}' not found")

        if spell_name not in self.spells:
            self.spells.append(spell_name)
            self.save()

    def to_dict(self):
        """Convert NPC to dictionary."""
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'race': self.race,
            'npc_class': self.npc_class,
            'level': self.level,
            'background': self.background,
            'personality': self.personality,
            'abilities': self.abilities,
            'skills': self.skills,
            'equipment': self.equipment,
            'spells': self.spells,
            'description': self.description,
            'portrait_url': self.portrait_url
        }

    def save(self):
        """Save NPC to database."""
        npc_dict = self.to_dict()
        if self._id:
            self.mongo.db.npcs.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': {k: v for k, v in npc_dict.items() if k != '_id'}}
            )
        else:
            result = self.mongo.db.npcs.insert_one({k: v for k, v in npc_dict.items() if k != '_id'})
            self._id = result.inserted_id
        return self

    def delete(self):
        """Delete NPC from database."""
        if self._id:
            self.mongo.db.npcs.delete_one({'_id': ObjectId(self._id)})
