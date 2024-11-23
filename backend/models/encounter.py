from typing import List, Dict, Any
from .npc import NPC
from backend.utils.dnd_api_client import DnDApiClient
from flask_pymongo import PyMongo
from bson import ObjectId

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
        monsters (list): List of monster names from D&D 5e
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
            monsters (list, optional): List of monster names. Defaults to None.
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

    def add_monster(self, monster_name):
        """Add a monster to the encounter.

        This method validates the monster against the D&D 5e API and updates
        both the local state and database.

        Args:
            monster_name (str): Name of the monster to add

        Returns:
            tuple: (bool, str) - Success status and message

        Raises:
            ValueError: If monster_name is invalid or API request fails
            RuntimeError: If database operation fails
        """
        if not self.mongo:
            from flask import current_app
            self.mongo = current_app.mongo

        try:
            if monster_name not in self.monsters:
                # Get monster details from DnD API
                dnd_api = DnDApiClient()
                try:
                    monster = dnd_api.get_monster(monster_name)
                    if not monster:
                        return False, f"Monster '{monster_name}' not found in DnD API"
                except Exception as e:
                    raise ValueError(f"Failed to fetch monster details: {str(e)}")

                try:
                    self.monsters.append(monster_name)
                    self.mongo.db.encounters.update_one(
                        {'_id': ObjectId(self._id)},
                        {'$push': {'monsters': monster_name}}
                    )
                    return True, f"Successfully added monster '{monster_name}'"
                except Exception as e:
                    # Rollback the local state change if db update fails
                    self.monsters.remove(monster_name)
                    raise RuntimeError(f"Failed to update database: {str(e)}")

            return False, f"Monster '{monster_name}' already exists in encounter"
        except ValueError as ve:
            raise ve
        except RuntimeError as re:
            raise re
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

    def remove_monster(self, monster_name):
        """Remove a monster from the encounter.

        Args:
            monster_name (str): Name of the monster to remove

        Returns:
            bool: True if monster was removed successfully

        Raises:
            RuntimeError: If database operation fails
        """
        try:
            if not self.mongo:
                from flask import current_app
                self.mongo = current_app.mongo

            if monster_name in self.monsters:
                self.monsters.remove(monster_name)
                self.mongo.db.encounters.update_one(
                    {'_id': ObjectId(self._id)},
                    {'$pull': {'monsters': monster_name}}
                )
                return True
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to remove monster: {str(e)}")

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
