import unittest
from backend.utils.dnd_api_client import DnDApiClient
from unittest.mock import patch

class TestDnDApiClient(unittest.TestCase):
    def setUp(self):
        self.client = DnDApiClient()

    @patch('backend.utils.dnd_api_client.requests.get')
    def test_get_monster(self, mock_get):
        mock_response = {
            'name': 'Goblin',
            'hit_points': 7
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = self.client.get_monster('goblin')
        self.assertEqual(result['name'], 'Goblin')
        self.assertEqual(result['hit_points'], 7)
        mock_get.assert_called_once_with('https://www.dnd5eapi.co/api/monsters/goblin')

if __name__ == '__main__':
    unittest.main()
