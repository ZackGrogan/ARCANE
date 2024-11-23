from bson import ObjectId
from typing import Dict, Any, List, Optional, Union

class Campaign:
    def __init__(self, mongo, title: str, description: str = '', setting: str = '',
                 dm_notes: str = '', npcs: Optional[List[str]] = None,
                 encounters: Optional[List[str]] = None, _id: Optional[Union[str, ObjectId]] = None):
        """Initialize a campaign."""
        self.mongo = mongo
        self._id = ObjectId(_id) if _id else ObjectId()
        self.title = self._validate_title(title)
        self.description = description
        self.setting = setting
        self.dm_notes = dm_notes
        self.npcs = [str(npc_id) if isinstance(npc_id, ObjectId) else npc_id for npc_id in (npcs or [])]
        self.encounters = [str(enc_id) if isinstance(enc_id, ObjectId) else enc_id for enc_id in (encounters or [])]

    def _validate_title(self, title: str) -> str:
        """Validate campaign title."""
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        # Check for duplicate title only when creating new campaign
        if not hasattr(self, '_id'):
            existing = self.mongo.db.campaigns.find_one({'title': title})
            if existing and str(existing['_id']) != str(self._id):
                raise ValueError(f"Campaign '{title}' already exists")
        return title

    def save(self) -> bool:
        """Save campaign to database."""
        campaign_data = self.to_dict()
        # Convert string ID back to ObjectId for MongoDB
        campaign_data['_id'] = self._id
        if not self.mongo.db.campaigns.find_one({'_id': self._id}):
            self.mongo.db.campaigns.insert_one(campaign_data)
        else:
            self.mongo.db.campaigns.update_one(
                {'_id': self._id},
                {'$set': campaign_data}
            )
        return True

    def delete(self) -> bool:
        """Delete campaign from database."""
        result = self.mongo.db.campaigns.delete_one({'_id': self._id})
        return result.deleted_count > 0

    def add_npc(self, npc_id: str) -> bool:
        """Add an NPC to the campaign."""
        npc_id = str(npc_id)
        if npc_id not in self.npcs:
            self.npcs.append(npc_id)
            self.save()
        return True

    def remove_npc(self, npc_id: str) -> bool:
        """Remove an NPC from the campaign."""
        npc_id = str(npc_id)
        if npc_id in self.npcs:
            self.npcs.remove(npc_id)
            self.save()
        return True

    def add_encounter(self, encounter_id: str) -> bool:
        """Add an encounter to the campaign."""
        encounter_id = str(encounter_id)
        if encounter_id not in self.encounters:
            self.encounters.append(encounter_id)
            self.save()
        return True

    def remove_encounter(self, encounter_id: str) -> bool:
        """Remove an encounter from the campaign."""
        encounter_id = str(encounter_id)
        if encounter_id in self.encounters:
            self.encounters.remove(encounter_id)
            self.save()
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert campaign to dictionary."""
        return {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'setting': self.setting,
            'dm_notes': self.dm_notes,
            'npcs': self.npcs,
            'encounters': self.encounters
        }

    @staticmethod
    def list_campaigns(mongo):
        """Get all campaigns."""
        campaigns = list(mongo.db.campaigns.find())
        for campaign in campaigns:
            campaign['_id'] = str(campaign['_id'])
        return campaigns
