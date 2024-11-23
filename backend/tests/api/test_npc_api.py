"""Test NPC API endpoints."""
import pytest
from unittest.mock import patch
from flask import url_for
from bson import ObjectId
from backend.models.npc import NPC
from backend.utils.errors import APIError

@pytest.fixture
def test_npc():
    """Test NPC data."""
    return {
        'name': 'Test NPC',
        'race': 'Human',
        'npc_class': 'Fighter',
        'level': 1,
        'alignment': 'True Neutral',
        'abilities': {
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 10,
            'wisdom': 10,
            'charisma': 10
        },
        'skills': [],
        'equipment': [],
        'spells': [],
        'background': None,
        'personality': None,
        'description': None,
        'portrait_url': None
    }

def test_create_npc(app, client, mongo, test_npc):
    """Test creating a new NPC."""
    with app.app_context():
        response = client.post('/api/npcs/', json=test_npc)
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == test_npc['name']
        assert data['race'] == test_npc['race']

def test_create_npc_invalid_data(app, client, mongo):
    """Test creating an NPC with invalid data."""
    with app.app_context():
        invalid_npc = {'name': 'Invalid NPC'}  # Missing required fields
        response = client.post('/api/npcs/', json=invalid_npc)
        assert response.status_code == 400
        assert 'error' in response.get_json()

def test_get_npc(app, client, mongo, test_npc):
    """Test retrieving an NPC."""
    with app.app_context():
        # First create an NPC
        response = client.post('/api/npcs/', json=test_npc)
        assert response.status_code == 201
        npc_id = response.get_json()['_id']

        # Then retrieve it
        response = client.get(f'/api/npcs/{npc_id}/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == test_npc['name']
        assert data['race'] == test_npc['race']

def test_get_nonexistent_npc(app, client, mongo):
    """Test retrieving a nonexistent NPC."""
    with app.app_context():
        response = client.get('/api/npcs/nonexistent/')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'NPC not found'

def test_update_npc(app, client, mongo, test_npc):
    """Test updating an NPC."""
    with app.app_context():
        # First create an NPC
        response = client.post('/api/npcs/', json=test_npc)
        assert response.status_code == 201
        npc_id = response.get_json()['_id']

        # Then update it
        update_data = {'name': 'Updated NPC Name'}
        response = client.put(f'/api/npcs/{npc_id}/', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == update_data['name']
        assert data['race'] == test_npc['race']  # Other fields should remain unchanged

def test_update_nonexistent_npc(app, client, mongo):
    """Test updating a nonexistent NPC."""
    with app.app_context():
        update_data = {'name': 'Updated NPC Name'}
        response = client.put('/api/npcs/nonexistent/', json=update_data)
        assert response.status_code == 404
        assert response.get_json()['error'] == 'NPC not found'

def test_delete_npc(app, client, mongo, test_npc):
    """Test deleting an NPC."""
    with app.app_context():
        # First create an NPC
        response = client.post('/api/npcs/', json=test_npc)
        assert response.status_code == 201
        npc_id = response.get_json()['_id']

        # Then delete it
        response = client.delete(f'/api/npcs/{npc_id}/')
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f'/api/npcs/{npc_id}/')
        assert response.status_code == 404

def test_delete_nonexistent_npc(app, client, mongo):
    """Test deleting a nonexistent NPC."""
    with app.app_context():
        response = client.delete('/api/npcs/nonexistent/')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'NPC not found'

def test_list_npcs(app, client, mongo, test_npc):
    """Test listing all NPCs."""
    with app.app_context():
        # Initially there should be no NPCs
        response = client.get('/api/npcs/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0

        # Create a few NPCs
        npcs_to_create = [
            test_npc,
            {**test_npc, 'name': 'Test NPC 2'},
            {**test_npc, 'name': 'Test NPC 3'}
        ]
        for npc in npcs_to_create:
            response = client.post('/api/npcs/', json=npc)
            assert response.status_code == 201

        # List all NPCs
        response = client.get('/api/npcs/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == len(npcs_to_create)
        assert all('_id' in npc for npc in data)
