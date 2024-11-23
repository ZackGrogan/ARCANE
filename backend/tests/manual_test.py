"""Manual testing script for API endpoints."""
import json
from pprint import pprint
from backend import create_app

# Create application and test client globally
app = create_app({
    'TESTING': True,
    'MONGO_URI': 'mongodb://localhost:27017/test_db'
})
client = app.test_client()

def test_npc_endpoints():
    """Test NPC endpoints."""
    with app.app_context():
        print("\n=== Testing NPC Endpoints ===")

        # Test NPC creation with valid data
        print("\n1. Creating NPC with valid data")
        valid_npc = {
            'name': 'Test NPC',
            'race': 'Human',
            'npc_class': 'Fighter',
            'level': 5,
            'alignment': 'Lawful Good',
            'abilities': {
                'strength': 16,
                'dexterity': 14,
                'constitution': 15,
                'intelligence': 12,
                'wisdom': 13,
                'charisma': 11
            }
        }
        try:
            response = client.post('/api/npcs', json=valid_npc)
            print(f"Status: {response.status_code}")
            print("Response:")
            response_data = json.loads(response.data)
            pprint(response_data)
            npc_id = response_data.get('_id')
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")
            return

        # Test NPC creation with invalid data
        print("\n2. Creating NPC with invalid data (missing required fields)")
        invalid_npc = {
            'name': 'Invalid NPC'
        }
        try:
            response = client.post('/api/npcs', json=invalid_npc)
            print(f"Status: {response.status_code}")
            print("Response:")
            pprint(json.loads(response.data))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")

        # Get all NPCs
        print("\n4. Getting all NPCs")
        try:
            response = client.get('/api/npcs')
            print(f"Status: {response.status_code}")
            print("Response:")
            pprint(json.loads(response.data))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")

def test_campaign_endpoints():
    """Test Campaign endpoints."""
    with app.app_context():
        print("\n=== Testing Campaign Endpoints ===")

        # Test Campaign creation
        print("\n1. Creating Campaign")
        campaign_data = {
            'title': 'Test Campaign',
            'description': 'A test campaign',
            'start_date': '2024-01-01',
            'status': 'active',
            'notes': 'Test notes'
        }
        try:
            response = client.post('/api/campaigns', json=campaign_data)
            print(f"Status: {response.status_code}")
            print("Response:")
            response_data = json.loads(response.data)
            pprint(response_data)
            campaign_id = response_data.get('_id')
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")
            return

        # Get all campaigns
        print("\n2. Getting all campaigns")
        try:
            response = client.get('/api/campaigns')
            print(f"Status: {response.status_code}")
            print("Response:")
            pprint(json.loads(response.data))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")

def test_encounter_endpoints():
    """Test Encounter endpoints."""
    with app.app_context():
        print("\n=== Testing Encounter Endpoints ===")

        # Test Encounter creation
        print("\n1. Creating Encounter")
        encounter_data = {
            'title': 'Test Encounter',
            'environment': 'Forest',
            'party_level': 5,
            'difficulty': 'Medium',
            'notes': 'A test encounter',
            'monsters': ['Goblin', 'Wolf'],
            'traps': ['Pit Trap']
        }
        try:
            response = client.post('/api/encounters', json=encounter_data)
            print(f"Status: {response.status_code}")
            print("Response:")
            response_data = json.loads(response.data)
            pprint(response_data)
            encounter_id = response_data.get('_id')
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")
            return

        # Get all encounters
        print("\n2. Getting all encounters")
        try:
            response = client.get('/api/encounters')
            print(f"Status: {response.status_code}")
            print("Response:")
            pprint(json.loads(response.data))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.data}")

def main():
    """Run all manual tests."""
    test_npc_endpoints()
    test_campaign_endpoints()
    test_encounter_endpoints()

if __name__ == '__main__':
    main()
