from typing import List, Dict, Any
from .npc import NPC
from backend.utils.dnd_api_client import DnDApiClient
from flask_pymongo import PyMongo
from bson import ObjectId
from backend.utils.errors import APIError

class Encounter:
    """Encounter model for managing D&D combat encounters.

    This class handles the creation, modification, and management of combat encounters,
    including monster management and database operations.

    Attributes:
        mongo: MongoDB connection instance
        title (str): Unique title of the encounter
        environment (str): Type of environment (e.g., dungeon, forest)
        party_level (int): Average level of the party
        difficulty (str): Encounter difficulty (easy, medium, hard, deadly)
        description (str): Optional description of the encounter
        monsters (list): List of monster objects
        traps (list): List of trap objects
        notes (str): Additional notes about the encounter
        _id: MongoDB ObjectId for the encounter
        _updated_fields (set): Tracks which fields have been modified
    """

    def __init__(self, mongo, title, environment, party_level, difficulty,
                 description='', monsters=None, traps=None, notes='', _id=None):
        """Initialize an encounter.

        Args:
            mongo: MongoDB connection instance
            title (str): Unique title of the encounter
            environment (str): Type of environment
            party_level (int): Average level of the party
            difficulty (str): Encounter difficulty
            description (str, optional): Description of the encounter. Defaults to ''.
            monsters (list, optional): List of monster objects. Defaults to None.
            traps (list, optional): List of trap objects. Defaults to None.
            notes (str, optional): Additional notes. Defaults to ''.
            _id (ObjectId, optional): MongoDB ObjectId. Defaults to None.
        """
        self.mongo = mongo
        self.title = title
        self.environment = environment
        self.party_level = party_level
        self.difficulty = difficulty
        self.description = description
        self.monsters = monsters or []
        self.traps = traps or []
        self.notes = notes
        self._id = _id
        self._updated_fields = set()

    def to_dict(self):
        """Convert encounter to dictionary format.

        Returns:
            dict: Dictionary representation of the encounter, including all fields
                  and the MongoDB ObjectId as a string.
        """
        result = {
            'title': self.title,
            'environment': self.environment,
            'party_level': self.party_level,
            'difficulty': self.difficulty,
            'description': self.description,
            'monsters': self.monsters,
            'traps': self.traps,
            'notes': self.notes
        }
        if self._id:
            result['_id'] = str(self._id)
        return result

    def save(self):
        """Save encounter to database.

        This method handles both creation of new encounters and updates to existing ones.
        It includes validation for title uniqueness and proper ObjectId handling.

        Returns:
            bool: True if save was successful, False otherwise

        Raises:
            ValueError: If title is not unique
            RuntimeError: If database operation fails
        """
        try:
            # Check for title uniqueness (case-insensitive)
            existing = self.mongo.db.encounters.find_one({
                'title': {'$regex': f'^{self.title}$', '$options': 'i'},
                '_id': {'$ne': ObjectId(self._id) if self._id else None}
            })
            if existing:
                raise ValueError(f"Encounter with title '{self.title}' already exists")

            encounter_data = self.to_dict()
            if '_id' in encounter_data:
                del encounter_data['_id']

            if self._id:
                # Update existing encounter
                result = self.mongo.db.encounters.update_one(
                    {'_id': ObjectId(self._id)},
                    {'$set': encounter_data}
                )
                return result.modified_count > 0
            else:
                # Create new encounter
                result = self.mongo.db.encounters.insert_one(encounter_data)
                self._id = result.inserted_id
                return bool(result.inserted_id)
        except Exception as e:
            raise RuntimeError(f"Failed to save encounter: {str(e)}")

    def update(self, data):
        """Update encounter with new data.

        Args:
            data (dict): Dictionary of fields to update

        Returns:
            bool: True if update was successful

        Raises:
            ValueError: If title update would create a duplicate
            RuntimeError: If database operation fails
        """
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    self._updated_fields.add(key)
            return self.save()
        except Exception as e:
            raise RuntimeError(f"Failed to update encounter: {str(e)}")

    def delete(self):
        """Delete encounter from database.

        Returns:
            bool: True if deletion was successful

        Raises:
            RuntimeError: If database operation fails
        """
        try:
            if not self._id:
                return False
            result = self.mongo.db.encounters.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to delete encounter: {str(e)}")

    def add_monster(self, monster_name, quantity=1):
        """Add a monster to the encounter.

        Args:
            monster_name (str): Name of the monster to add
            quantity (int, optional): Number of monsters to add. Defaults to 1.

        Returns:
            tuple: (success, message) where success is a boolean and message is a string

        Raises:
            APIError: If monster already exists or if there's an error with the DnD API
        """
        monster_name = monster_name.strip().title()

        # Check for existing monster
        if any(m['name'].lower() == monster_name.lower() for m in self.monsters):
            raise APIError(f"Monster '{monster_name}' already exists in encounter", 400)

        # Get monster details from DnD API
        try:
            dnd_api = DnDApiClient()
            monster_details = dnd_api.get_monster(monster_name)
            if not monster_details:
                raise APIError(f"Monster '{monster_name}' not found", 404)

            monster_entry = {
                'name': monster_name,
                'quantity': quantity,
                'challenge_rating': monster_details.get('challenge_rating', 0),
                'hit_points': monster_details.get('hit_points', 0)
            }

            self.monsters.append(monster_entry)
            if self.save():
                return True, f"Successfully added {quantity} {monster_name}(s)"
            return False, "Failed to save encounter"

        except APIError:
            raise
        except Exception as e:
            raise APIError(f"Error adding monster: {str(e)}", 500)

    def remove_monster(self, monster_name):
        """Remove a monster from the encounter."""
        monster_name = monster_name.strip().title()

        initial_count = len(self.monsters)
        self.monsters = [
            m for m in self.monsters
            if m['name'].lower() != monster_name.lower()
        ]

        if len(self.monsters) == initial_count:
            return False

        return self.save()

    @classmethod
    def list_encounters(cls, mongo):
        """List all encounters in the database.

        Args:
            mongo: MongoDB connection instance

        Returns:
            list: List of Encounter objects

        Raises:
            RuntimeError: If database operation fails
        """
        try:
            encounters = []
            for encounter_data in mongo.db.encounters.find():
                encounter = cls.from_dict(mongo, encounter_data)
                encounters.append(encounter)
            return encounters
        except Exception as e:
            raise RuntimeError(f"Failed to list encounters: {str(e)}")

    @classmethod
    def get_encounter(cls, mongo, _id):
        """Get an encounter by ID.

        Args:
            mongo: MongoDB connection instance
            _id: MongoDB ObjectId or string

        Returns:
            Encounter: Encounter object if found, None otherwise

        Raises:
            ValueError: If _id is invalid
            RuntimeError: If database operation fails
        """
        try:
            if isinstance(_id, str):
                _id = ObjectId(_id)
            encounter_data = mongo.db.encounters.find_one({'_id': _id})
            if encounter_data:
                return cls.from_dict(mongo, encounter_data)
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get encounter: {str(e)}")

    @classmethod
    def get_by_id(cls, mongo, encounter_id):
        """Get an encounter by its ID.

        Args:
            mongo: MongoDB connection instance
            encounter_id (str): ID of the encounter to retrieve

        Returns:
            Encounter: The encounter object if found, None otherwise
        """
        try:
            _id = ObjectId(encounter_id)
            encounter_data = mongo.db.encounters.find_one({'_id': _id})
            if encounter_data:
                return cls(
                    mongo=mongo,
                    title=encounter_data['title'],
                    environment=encounter_data['environment'],
                    party_level=encounter_data['party_level'],
                    difficulty=encounter_data['difficulty'],
                    description=encounter_data.get('description', ''),
                    monsters=encounter_data.get('monsters', []),
                    traps=encounter_data.get('traps', []),
                    notes=encounter_data.get('notes', ''),
                    _id=encounter_data['_id']
                )
            return None
        except Exception:
            return None

    @classmethod
    def from_dict(cls, mongo, data):
        """Create encounter from dictionary.

        Args:
            mongo: MongoDB connection instance
            data (dict): Dictionary containing encounter data

        Returns:
            Encounter: New Encounter object
        """
        _id = data.pop('_id', None)
        return cls(mongo=mongo, _id=_id, **data)
