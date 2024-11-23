"""Campaign model for managing D&D campaign data and related resources.

This module provides functionality for creating, managing, and tracking D&D campaigns,
including associated NPCs, encounters, and maps.
"""
from typing import List, Tuple, Dict, Any
from flask_pymongo import PyMongo
from bson import ObjectId
from .npc import NPC
from .encounter import Encounter

class Campaign:
    """Campaign model for managing D&D campaigns.

    This class handles the creation, modification, and management of D&D campaigns,
    including associated NPCs, encounters, and maps.

    Attributes:
        mongo (PyMongo): MongoDB connection instance
        name (str): Unique name of the campaign
        description (str): Detailed description of the campaign
        start_date (str): Campaign start date
        status (str): Current campaign status (active/completed/archived)
        notes (str): Additional campaign notes
        npcs (List[str]): List of NPC IDs associated with the campaign
        encounters (List[str]): List of encounter IDs associated with the campaign
        maps (List[str]): List of map URLs or references
        _id (ObjectId): MongoDB ObjectId for the campaign
    """

    def __init__(self, mongo: PyMongo, name: str, description: str, start_date: str,
                 status: str = 'active', notes: str = '', npcs: List[str] = None,
                 encounters: List[str] = None, maps: List[str] = None, _id: str = None):
        """Initialize a campaign with the specified attributes.

        Args:
            mongo (PyMongo): MongoDB connection instance
            name (str): Unique campaign name
            description (str): Campaign description
            start_date (str): Start date of the campaign
            status (str, optional): Campaign status. Defaults to 'active'.
            notes (str, optional): Additional notes. Defaults to ''.
            npcs (List[str], optional): List of NPC IDs. Defaults to None.
            encounters (List[str], optional): List of encounter IDs. Defaults to None.
            maps (List[str], optional): List of map references. Defaults to None.
            _id (str, optional): MongoDB ObjectId. Defaults to None.

        Raises:
            ValueError: If any validation fails
        """
        self.mongo = mongo
        self._id = ObjectId(_id) if _id else None
        self._validate_name(name)
        self._validate_description(description)
        self._validate_start_date(start_date)
        self._validate_status(status)
        self.name = name
        self.description = description
        self.start_date = start_date
        self.status = status
        self.notes = notes
        self.npcs = npcs if npcs is not None else []
        self.encounters = encounters if encounters is not None else []
        self.maps = maps if maps is not None else []

    def _validate_name(self, name: str) -> None:
        """Validate campaign name.

        Args:
            name (str): Campaign name to validate

        Raises:
            ValueError: If name is empty, too long, or not unique
        """
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 100:  # Add reasonable length limit
            raise ValueError("Name is too long (max 100 characters)")
        # Only check uniqueness when creating a new campaign (no _id)
        if not self._id and self.mongo is not None:
            existing = self.mongo.db.campaigns.find_one({'name': name})
            if existing:
                raise ValueError("A campaign with this name already exists")

    def _validate_description(self, description: str) -> None:
        """Validate campaign description.

        Args:
            description (str): Campaign description to validate

        Raises:
            ValueError: If description is empty
        """
        if not description:
            raise ValueError("Description cannot be empty")

    def _validate_start_date(self, start_date: str) -> None:
        """Validate campaign start date.

        Args:
            start_date (str): Campaign start date to validate

        Raises:
            ValueError: If start date is empty
        """
        if not start_date:
            raise ValueError("Start date cannot be empty")

    def _validate_status(self, status: str) -> None:
        """Validate campaign status.

        Args:
            status (str): Campaign status to validate

        Raises:
            ValueError: If status is not one of the valid options
        """
        valid_statuses = ['active', 'completed', 'on_hold', 'cancelled']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert campaign to dictionary format.

        Returns:
            Dict[str, Any]: Dictionary representation of the campaign
        """
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'status': self.status,
            'notes': self.notes,
            'npcs': self.npcs,
            'encounters': self.encounters,
            'maps': self.maps
        }

    def save(self) -> bool:
        """Save campaign to database.

        Returns:
            bool: True if save was successful

        Raises:
            RuntimeError: If database operation fails
        """
        data = self.to_dict()
        if '_id' in data:
            del data['_id']  # Remove _id from data to avoid duplicate key error

        if self._id:
            self.mongo.db.campaigns.update_one(
                {'_id': self._id},
                {'$set': data}
            )
        else:
            result = self.mongo.db.campaigns.insert_one(data)
            self._id = result.inserted_id
        return True

    def update(self, data: Dict[str, Any]) -> bool:
        """Update campaign with new data.

        Args:
            data (Dict[str, Any]): Dictionary of fields to update

        Returns:
            bool: True if update was successful

        Raises:
            ValueError: If validation fails
            RuntimeError: If database operation fails
        """
        if 'name' in data:
            if not isinstance(data['name'], str):
                raise ValueError("name must be a string")
            if not data['name']:
                raise ValueError("Name cannot be empty")
            if len(data['name']) > 100:
                raise ValueError("Name is too long (max 100 characters)")
            # Check if new name is already taken by another campaign
            if data['name'] != self.name:
                existing = self.mongo.db.campaigns.find_one({'name': data['name']})
                if existing and str(existing['_id']) != str(self._id):
                    raise ValueError("A campaign with this name already exists")
            self.name = data['name']

        if 'description' in data:
            self._validate_description(data['description'])
            self.description = data['description']
        if 'start_date' in data:
            self._validate_start_date(data['start_date'])
            self.start_date = data['start_date']
        if 'status' in data:
            self._validate_status(data['status'])
            self.status = data['status']
        if 'notes' in data:
            self.notes = data['notes']
        if 'npcs' in data:
            self.npcs = data['npcs']
        if 'encounters' in data:
            self.encounters = data['encounters']
        if 'maps' in data:
            self.maps = data['maps']
        self.save()
        return True

    def delete(self) -> bool:
        """Delete campaign from database.

        Returns:
            bool: True if deletion was successful

        Raises:
            RuntimeError: If database operation fails
        """
        if self._id:
            self.mongo.db.campaigns.delete_one({'_id': self._id})
        return True

    def update_progress(self, completed_encounters: int, total_encounters: int):
        """Update campaign progress.

        Args:
            completed_encounters (int): Number of completed encounters
            total_encounters (int): Total number of encounters

        Returns:
            None
        """
        if total_encounters > 0:
            progress = (completed_encounters / total_encounters) * 100
            self.update({'progress': progress})
        else:
            self.update({'progress': 0})

    def add_npc(self, npc_id: str):
        """Add NPC to campaign.

        Args:
            npc_id (str): ID of NPC to add

        Returns:
            None
        """
        if npc_id not in self.npcs:
            self.npcs.append(npc_id)
            self.update({'npcs': self.npcs})

    def remove_npc(self, npc_id: str):
        """Remove NPC from campaign.

        Args:
            npc_id (str): ID of NPC to remove

        Returns:
            None
        """
        if npc_id in self.npcs:
            self.npcs.remove(npc_id)
            self.update({'npcs': self.npcs})

    def add_encounter(self, encounter_id: str):
        """Add encounter to campaign.

        Args:
            encounter_id (str): ID of encounter to add

        Returns:
            None
        """
        if encounter_id not in self.encounters:
            self.encounters.append(encounter_id)
            self.update({'encounters': self.encounters})

    def remove_encounter(self, encounter_id: str):
        """Remove encounter from campaign.

        Args:
            encounter_id (str): ID of encounter to remove

        Returns:
            None
        """
        if encounter_id in self.encounters:
            self.encounters.remove(encounter_id)
            self.update({'encounters': self.encounters})

    @classmethod
    def get_by_name(cls, mongo: PyMongo, name: str) -> 'Campaign':
        """Get campaign by name.

        Args:
            mongo (PyMongo): MongoDB connection instance
            name (str): Campaign name to retrieve

        Returns:
            Campaign: Campaign object if found

        Raises:
            ValueError: If name is invalid
            RuntimeError: If database operation fails
        """
        campaign_data = mongo.db.campaigns.find_one({'name': name})
        if campaign_data:
            return Campaign.from_dict(mongo, campaign_data)
        return None

    @classmethod
    def get_campaign(cls, mongo: PyMongo, campaign_id: str) -> 'Campaign':
        """Get campaign by ID.

        Args:
            mongo (PyMongo): MongoDB connection instance
            campaign_id (str): Campaign ID to retrieve

        Returns:
            Campaign: Campaign object if found

        Raises:
            ValueError: If campaign_id is invalid
            RuntimeError: If database operation fails
        """
        campaign_data = mongo.db.campaigns.find_one({'_id': ObjectId(campaign_id)})
        if campaign_data:
            return Campaign.from_dict(mongo, campaign_data)
        return None

    @classmethod
    def list_campaigns(cls, mongo: PyMongo) -> List['Campaign']:
        """List all campaigns.

        Args:
            mongo (PyMongo): MongoDB connection instance

        Returns:
            List[Campaign]: List of all campaigns

        Raises:
            RuntimeError: If database operation fails
        """
        campaigns = []
        for campaign_data in mongo.db.campaigns.find():
            campaign = Campaign.from_dict(mongo, campaign_data)
            campaigns.append(campaign)
        return campaigns

    @classmethod
    def from_dict(cls, mongo, data):
        """Create a campaign from a dictionary.

        Args:
            mongo (PyMongo): MongoDB connection instance
            data (Dict[str, Any]): Dictionary representation of the campaign

        Returns:
            Campaign: Campaign object
        """
        return Campaign(
            mongo=mongo,
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'],
            status=data.get('status', 'active'),
            notes=data.get('notes', ''),
            npcs=data.get('npcs', []),
            encounters=data.get('encounters', []),
            maps=data.get('maps', []),
            _id=str(data['_id']) if '_id' in data else None
        )
