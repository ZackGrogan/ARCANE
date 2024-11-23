"""Unit tests for models."""
import pytest
from backend.models.npc import NPC
from backend.models.campaign import Campaign
from backend.models.encounter import Encounter

def test_npc_creation():
    """Test NPC model creation."""
    npc = NPC(None, name="Test NPC", race="Human", npc_class="Fighter")
    assert npc.name == "Test NPC"
    assert npc.race == "Human"
    assert npc.npc_class == "Fighter"
    assert npc.equipment == []
    assert npc.spells == []

def test_campaign_creation():
    """Test Campaign model creation."""
    campaign = Campaign(None, name="Test Campaign", description="Test Description", start_date="2024-03-14")
    assert campaign.name == "Test Campaign"
    assert campaign.description == "Test Description"
    assert campaign.start_date == "2024-03-14"
    assert campaign.status == "active"  # Default value
    assert campaign.notes == ""  # Default value
    assert campaign.npcs == []
    assert campaign.encounters == []
    assert campaign.maps == []

def test_campaign_validation():
    """Test Campaign model validation."""
    # Test empty name
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Campaign(None, name="", description="Test", start_date="2024-03-14")

    # Test empty description
    with pytest.raises(ValueError, match="Description cannot be empty"):
        Campaign(None, name="Test", description="", start_date="2024-03-14")

    # Test empty start_date
    with pytest.raises(ValueError, match="Start date cannot be empty"):
        Campaign(None, name="Test", description="Test", start_date="")

    # Test invalid status
    with pytest.raises(ValueError, match="Status must be one of:"):
        Campaign(None, name="Test", description="Test", start_date="2024-03-14", status="invalid")

def test_encounter_creation():
    """Test Encounter model creation."""
    encounter = Encounter(None, title="Test Encounter", environment="Forest", party_level=5, difficulty="Medium")
    assert encounter.title == "Test Encounter"
    assert encounter.environment == "Forest"
    assert encounter.party_level == 5
    assert encounter.difficulty == "Medium"
