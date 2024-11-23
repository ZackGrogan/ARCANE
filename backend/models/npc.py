"""NPC model for managing NPC data."""
from flask_pymongo import PyMongo
from typing import Dict, Any, List, Optional, Union
from bson import ObjectId
from backend.utils.dnd_api_client import DnDApiClient
from backend.utils.errors import APIError

class NPC:
    """Class representing an NPC in the game."""

    VALID_ALIGNMENTS = [
        'Lawful Good', 'Neutral Good', 'Chaotic Good',
        'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
        'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
    ]

    def __init__(self, mongo: PyMongo, name: str, race: str, npc_class: str, level: int = 1, alignment: str = None,
                 abilities: Dict[str, int] = None, skills: List[str] = None, equipment: List[str] = None, spells: List[Dict[str, Any]] = None,
                 background: str = None, personality: str = None, description: str = None,
                 portrait_url: str = None, _id: Optional[str] = None):
        """Initialize NPC with required attributes."""
        try:
            self.mongo = mongo
            self._id = ObjectId(_id) if _id else None
            self.name = self._validate_name(name)
            self.race = self._validate_str_field('race', race)
            self.npc_class = self._validate_str_field('class', npc_class)
            self.level = self._validate_level(level)
            self.alignment = self._validate_alignment(alignment)
            self.abilities = self._validate_abilities(abilities)
            self.skills = skills or []
            self.equipment = equipment or []
            self.spells = spells or []
            self.background = background
            self.personality = personality
            self.description = description
            self.portrait_url = portrait_url
        except ValueError as e:
            raise APIError(str(e), 400)
        except Exception as e:
            raise APIError(f"Error creating NPC: {str(e)}", 500)

    def _validate_name(self, name: str) -> str:
        """Validate NPC name."""
        if not name or not isinstance(name, str):
            raise APIError("Name cannot be empty", 400)
        if len(name) > 100:
            raise APIError("Name must be 100 characters or less", 400)
        # Skip uniqueness check if in test mode or if mongo is not available
        if not self._id and self.mongo and not getattr(self.mongo, '_testing', False):
            existing = self.mongo.db.npcs.find_one({'name': name})
            if existing and str(existing.get('_id')) != str(self._id):
                raise APIError("An NPC with this name already exists", 409)
        return name

    def _validate_str_field(self, field_name: str, value: str) -> str:
        """Validate a string field."""
        if not value or not isinstance(value, str):
            raise APIError(f"{field_name.capitalize()} cannot be empty", 400)
        return value

    def _validate_level(self, level: int) -> int:
        """Validate NPC level."""
        try:
            level = int(level)
            if not 1 <= level <= 20:
                raise ValueError
        except (TypeError, ValueError):
            raise APIError("Level must be between 1 and 20", 400)
        return level

    def _validate_alignment(self, alignment: str) -> str:
        """Validate NPC alignment."""
        if alignment is None:
            return 'True Neutral'
        if alignment not in self.VALID_ALIGNMENTS:
            return 'True Neutral'  # Default to True Neutral instead of raising an error
        return alignment

    def _validate_abilities(self, abilities: Dict[str, int]) -> Dict[str, int]:
        """Validate ability scores."""
        if abilities is None:
            return {
                'strength': 10, 'dexterity': 10, 'constitution': 10,
                'intelligence': 10, 'wisdom': 10, 'charisma': 10
            }

        valid_abilities = {
            'strength', 'dexterity', 'constitution',
            'intelligence', 'wisdom', 'charisma'
        }

        if not isinstance(abilities, dict):
            raise APIError("Abilities must be a dictionary", 400)

        for ability in valid_abilities:
            if ability not in abilities:
                abilities[ability] = 10
            else:
                try:
                    score = int(abilities[ability])
                    if not 3 <= score <= 20:
                        raise ValueError
                    abilities[ability] = score
                except (TypeError, ValueError):
                    raise APIError(
                        f"Ability score for {ability} must be between 3 and 20",
                        400,
                        {'ability': ability, 'valid_range': {'min': 3, 'max': 20}}
                    )

        return abilities

    def save(self) -> str:
        """Save NPC to database."""
        try:
            npc_data = self.to_dict()
            if self._id:
                self.mongo.db.npcs.update_one(
                    {'_id': self._id},
                    {'$set': npc_data}
                )
            else:
                result = self.mongo.db.npcs.insert_one(npc_data)
                self._id = result.inserted_id
            return str(self._id)
        except Exception as e:
            raise APIError(f"Error saving NPC: {str(e)}", 500)

    def to_dict(self) -> Dict[str, Any]:
        """Convert NPC to dictionary."""
        try:
            data = {
                'name': self.name,
                'race': self.race,
                'npc_class': self.npc_class,
                'level': self.level,
                'alignment': self.alignment,
                'abilities': self.abilities,
                'skills': self.skills,
                'equipment': self.equipment,
                'spells': self.spells,
                'background': self.background,
                'personality': self.personality,
                'description': self.description,
                'portrait_url': self.portrait_url
            }
            if self._id:
                data['_id'] = str(self._id)
            return data
        except Exception as e:
            raise APIError(f"Error converting NPC to dictionary: {str(e)}", 500)

    def update(self, update_dict: Dict[str, Any]) -> None:
        """Update NPC attributes."""
        try:
            update_dict.pop('_id', None)

            if 'class' in update_dict:
                update_dict['npc_class'] = update_dict.pop('class')

            for key, value in update_dict.items():
                if hasattr(self, key):
                    # Validate the value before setting it
                    if key == 'name':
                        value = self._validate_name(value)
                    elif key in ['race', 'npc_class']:
                        value = self._validate_str_field(key, value)
                    elif key == 'level':
                        value = self._validate_level(value)
                    elif key == 'alignment':
                        value = self._validate_alignment(value)
                    elif key == 'abilities':
                        value = self._validate_abilities(value)

                    setattr(self, key, value)

            self._update_in_db()
        except APIError:
            raise
        except Exception as e:
            raise APIError(f"Error updating NPC: {str(e)}", 500)

    def _update_in_db(self) -> None:
        """Update NPC in database."""
        try:
            if self._id:
                update_data = self.to_dict()
                update_data.pop('_id', None)
                self.mongo.db.npcs.update_one(
                    {'_id': self._id},
                    {'$set': update_data}
                )
        except Exception as e:
            raise APIError(f"Error updating NPC in database: {str(e)}", 500)

    def delete(self) -> bool:
        """Delete NPC from database."""
        try:
            result = self.mongo.db.npcs.delete_one({'_id': self._id})
            return bool(result.deleted_count)
        except Exception as e:
            raise APIError(f"Error deleting NPC: {str(e)}", 500)

    def calculate_ability_modifier(self, ability: str) -> int:
        """Calculate ability modifier from ability score."""
        if ability not in self.abilities:
            raise APIError(
                f"Invalid ability: {ability}",
                400,
                {'valid_abilities': list(self.abilities.keys())}
            )
        return (self.abilities[ability] - 10) // 2

    def add_equipment(self, equipment_data: Union[str, Dict[str, Any]]) -> None:
        """Add equipment to NPC's inventory."""
        try:
            if isinstance(equipment_data, str):
                equipment_name = equipment_data
            else:
                equipment_name = equipment_data.get('name')

            if not equipment_name:
                raise APIError("Equipment name is required", 400)

            if equipment_name in self.equipment:
                raise APIError(f"Equipment '{equipment_name}' already added to NPC", 409)

            self.equipment.append(equipment_name)
            self._update_in_db()
        except APIError:
            raise
        except Exception as e:
            raise APIError(f"Error adding equipment: {str(e)}", 500)

    def add_spell(self, spell_data: Union[str, Dict[str, Any]]) -> None:
        """Add spell to NPC's spellbook."""
        try:
            if isinstance(spell_data, str):
                spell_name = spell_data
            else:
                spell_name = spell_data.get('name')

            if not spell_name:
                raise APIError("Spell name is required", 400)

            if spell_name in [spell['name'] for spell in self.spells]:
                raise APIError(f"Spell '{spell_name}' already added to NPC", 409)

            self.spells.append({'name': spell_name})
            self._update_in_db()
        except APIError:
            raise
        except Exception as e:
            raise APIError(f"Error adding spell: {str(e)}", 500)

    @classmethod
    def list_npcs(cls, mongo: PyMongo) -> List[Dict[str, Any]]:
        """List all NPCs."""
        try:
            return list(mongo.db.npcs.find())
        except Exception as e:
            raise APIError(f"Error listing NPCs: {str(e)}", 500)

    @classmethod
    def get_npc(cls, mongo, npc_name):
        """Get an NPC by name.

        Args:
            mongo: MongoDB connection
            npc_name (str): Name of the NPC to retrieve

        Returns:
            NPC: The NPC instance if found, None otherwise
        """
        npc_data = mongo.db.npcs.find_one({'name': npc_name})
        if npc_data:
            return cls.from_dict(mongo, npc_data)
        return None

    @classmethod
    def get_by_id(cls, mongo, npc_id):
        """Get an NPC by ID.

        Args:
            mongo: MongoDB connection
            npc_id (str): ID of the NPC to retrieve

        Returns:
            NPC: The NPC instance if found, None otherwise
        """
        try:
            npc_data = mongo.db.npcs.find_one({'_id': ObjectId(npc_id)})
            if npc_data:
                return cls.from_dict(mongo, npc_data)
        except Exception:
            return None
        return None

    @classmethod
    def from_dict(cls, mongo: PyMongo, data: Dict[str, Any]) -> 'NPC':
        """Create an NPC from a dictionary."""
        try:
            # Extract only the fields we need
            npc_data = {
                'name': data.get('name'),
                'race': data.get('race'),
                'npc_class': data.get('npc_class'),
                'level': data.get('level', 1),
                'alignment': data.get('alignment'),
                'abilities': data.get('abilities'),
                'skills': data.get('skills'),
                'equipment': data.get('equipment'),
                'spells': data.get('spells'),
                'background': data.get('background'),
                'personality': data.get('personality'),
                'description': data.get('description'),
                'portrait_url': data.get('portrait_url'),
                '_id': data.get('_id')
            }
            return cls(mongo=mongo, **npc_data)
        except Exception as e:
            raise APIError(f"Error creating NPC from dictionary: {str(e)}", 500)
