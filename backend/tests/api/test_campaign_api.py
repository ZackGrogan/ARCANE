"""Test Campaign API endpoints."""
import pytest
from flask import url_for
from bson import ObjectId

def test_create_campaign(app, client, db):
    """Test creating a new campaign."""
    with app.app_context():
        campaign_data = {
            'name': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-03-14',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        response = client.post('/api/campaigns/', json=campaign_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == campaign_data['name']
        assert data['description'] == campaign_data['description']
        assert data['start_date'] == campaign_data['start_date']
        assert data['status'] == campaign_data['status']

def test_get_campaign(app, client, db):
    """Test retrieving a single campaign."""
    with app.app_context():
        # First create a campaign
        campaign_data = {
            'name': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-03-14',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        create_response = client.post('/api/campaigns/', json=campaign_data)
        campaign_name = create_response.get_json()['name']

        # Then retrieve it
        response = client.get(f'/api/campaigns/{campaign_name}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == campaign_data['name']
        assert data['description'] == campaign_data['description']

def test_get_nonexistent_campaign(app, client, db):
    """Test retrieving a nonexistent campaign."""
    with app.app_context():
        response = client.get('/api/campaigns/nonexistent')
        assert response.status_code == 404
        assert 'error' in response.get_json()

def test_update_campaign(app, client, db):
    """Test updating a campaign."""
    with app.app_context():
        # First create a campaign
        campaign_data = {
            'name': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-03-14',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        create_response = client.post('/api/campaigns/', json=campaign_data)
        campaign_name = create_response.get_json()['name']

        # Update the campaign
        updated_data = {
            'description': 'Updated description',
            'status': 'completed'
        }
        response = client.put(f'/api/campaigns/{campaign_name}', json=updated_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['description'] == updated_data['description']
        assert data['status'] == updated_data['status']

def test_delete_campaign(app, client, db):
    """Test deleting a campaign."""
    with app.app_context():
        # First create a campaign
        campaign_data = {
            'name': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-03-14',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        create_response = client.post('/api/campaigns/', json=campaign_data)
        campaign_name = create_response.get_json()['name']

        # Delete the campaign
        response = client.delete(f'/api/campaigns/{campaign_name}')
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f'/api/campaigns/{campaign_name}')
        assert get_response.status_code == 404

def test_list_campaigns(app, client, db):
    """Test listing all campaigns."""
    with app.app_context():
        # Create a few campaigns
        campaign_data1 = {
            'name': 'Test Campaign 1',
            'description': 'A test campaign',
            'start_date': '2024-03-14',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        campaign_data2 = {
            'name': 'Test Campaign 2',
            'description': 'Another test campaign',
            'start_date': '2024-03-15',
            'status': 'active',
            'notes': '',
            'npcs': [],
            'encounters': [],
            'maps': []
        }
        client.post('/api/campaigns/', json=campaign_data1)
        client.post('/api/campaigns/', json=campaign_data2)

        # List all campaigns
        response = client.get('/api/campaigns/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert any(c['name'] == campaign_data1['name'] for c in data)
        assert any(c['name'] == campaign_data2['name'] for c in data)
