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
    """Test retrieving a single NPC."""
    with app.app_context():
        create_response = client.post('/api/npcs/', json=test_npc)
        assert create_response.status_code == 201
        npc_id = create_response.get_json()['_id']

        response = client.get(f'/api/npcs/{npc_id}/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == test_npc['name']
        assert data['race'] == test_npc['race']

def test_get_nonexistent_npc(app, client, mongo):
    """Test retrieving a nonexistent NPC."""
    with app.app_context():
        response = client.get(f'/api/npcs/{str(ObjectId())}/')
        assert response.status_code == 404
        assert 'error' in response.get_json()

def test_update_npc(app, client, mongo, test_npc):
    """Test updating an NPC."""
    with app.app_context():
        create_response = client.post('/api/npcs/', json=test_npc)
        assert create_response.status_code == 201
        npc_id = create_response.get_json()['_id']

        update_data = {'name': 'Updated NPC'}
        response = client.put(f'/api/npcs/{npc_id}/', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == update_data['name']

def test_update_nonexistent_npc(app, client, mongo):
    """Test updating a nonexistent NPC."""
    with app.app_context():
        update_data = {'name': 'Updated NPC'}
        response = client.put(f'/api/npcs/{str(ObjectId())}/', json=update_data)
        assert response.status_code == 404
        assert 'error' in response.get_json()

def test_delete_npc(app, client, mongo, test_npc):
    """Test deleting an NPC."""
    with app.app_context():
        create_response = client.post('/api/npcs/', json=test_npc)
        assert create_response.status_code == 201
        npc_id = create_response.get_json()['_id']

        response = client.delete(f'/api/npcs/{npc_id}/')
        assert response.status_code == 204

def test_delete_nonexistent_npc(app, client, mongo):
    """Test deleting a nonexistent NPC."""
    with app.app_context():
        response = client.delete(f'/api/npcs/{str(ObjectId())}/')
        assert response.status_code == 404
        assert 'error' in response.get_json()

def test_list_npcs(app, client, mongo, test_npc):
    """Test listing all NPCs."""
    with app.app_context():
        # Create multiple NPCs
        response1 = client.post('/api/npcs/', json=test_npc)
        assert response1.status_code == 201

        test_npc2 = dict(test_npc)
        test_npc2['name'] = 'Test NPC 2'
        response2 = client.post('/api/npcs/', json=test_npc2)
        assert response2.status_code == 201

        response = client.get('/api/npcs/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
