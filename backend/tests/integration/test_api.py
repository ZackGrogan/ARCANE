"""Integration tests for API endpoints."""
import pytest
from bson import ObjectId

@pytest.fixture
def test_npc():
    """Create a test NPC fixture."""
    return {
        'name': 'Test NPC',
        'race': 'Human',
        'npc_class': 'Fighter',
        'level': 5,
        'alignment': 'True Neutral',
        'background': 'Soldier',
        'personality': 'Brave and loyal',
        'bonds': 'Loyal to their unit',
        'flaws': 'Stubborn',
        'abilities': {
            'strength': 15,
            'dexterity': 14,
            'constitution': 13,
            'intelligence': 12,
            'wisdom': 10,
            'charisma': 8
        }
    }

def test_create_npc(client, test_npc):
    """Test NPC creation endpoint."""
    # Clear any existing NPCs
    with client.application.app_context():
        client.application.mongo.db.npcs.delete_many({})

    # Create NPC
    response = client.post('/api/npcs/', json=test_npc)
    assert response.status_code == 201, f"Failed to create NPC: {response.get_json()}"
    data = response.get_json()
    assert '_id' in data
    assert data['name'] == test_npc['name']

def test_get_npcs(client, db, test_npc):
    """Test getting all NPCs endpoint."""
    # Insert test NPC
    npc_id = db.npcs.insert_one(test_npc).inserted_id

    response = client.get('/api/npcs/')
    assert response.status_code == 200
    npcs = response.json
    assert len(npcs) > 0
    assert any(npc['name'] == test_npc['name'] for npc in npcs)

def test_create_campaign(client, test_campaign):
    """Test campaign creation endpoint."""
    response = client.post('/api/campaigns/', json=test_campaign)
    assert response.status_code == 201
    assert '_id' in response.json

def test_get_campaigns(client, db, test_campaign):
    """Test getting all campaigns endpoint."""
    # Insert test campaign
    campaign_id = db.campaigns.insert_one(test_campaign).inserted_id

    response = client.get('/api/campaigns/')
    assert response.status_code == 200
    campaigns = response.json
    assert len(campaigns) > 0
    assert any(campaign['name'] == test_campaign['name'] for campaign in campaigns)

def test_update_campaign(client, db, test_campaign):
    """Test updating a campaign endpoint."""
    # Insert test campaign
    campaign_id = db.campaigns.insert_one(test_campaign).inserted_id

    # Update campaign
    updates = {
        'description': 'Updated description',
        'status': 'completed'
    }
    response = client.put(f'/api/campaigns/{test_campaign["name"]}', json=updates)
    assert response.status_code == 200

    # Verify update
    updated = db.campaigns.find_one({'name': test_campaign['name']})
    assert updated['description'] == 'Updated description'
    assert updated['status'] == 'completed'

def test_create_encounter(client, test_encounter):
    """Test encounter creation endpoint."""
    response = client.post('/api/encounters/', json=test_encounter)
    assert response.status_code == 201
    assert '_id' in response.json

def test_get_encounters(client, db, test_encounter):
    """Test getting all encounters endpoint."""
    # Insert test encounter
    encounter_id = db.encounters.insert_one(test_encounter).inserted_id

    response = client.get('/api/encounters/')
    assert response.status_code == 200
    encounters = response.json
    assert len(encounters) > 0
    assert any(encounter['title'] == test_encounter['title'] for encounter in encounters)
