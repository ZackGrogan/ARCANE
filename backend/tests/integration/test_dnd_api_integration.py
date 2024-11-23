import os
import unittest
from unittest.mock import patch
import http.client
import json

from backend.utils.dnd_api_client import DnDApiClient
from backend.models.npc import NPC
from backend.models.encounter import Encounter

class TestDnDApiIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test app and client."""
        from backend import create_app
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.mongo = self.app.mongo

    @patch('http.client.HTTPConnection')
    def test_get_monster_success(self, mock_http_conn):
        mock_response = mock_http_conn.return_value.getresponse.return_value
        mock_response.status = 200
        mock_response.read.return_value = b'{"name": "Orc", "hit_points": 15}'
        client = DnDApiClient()
        result = client.get_monster('orc')
        self.assertEqual(result['name'], 'Orc')

    def test_npc_add_spell(self):
        """Test adding a spell to an NPC."""
        with self.app.app_context():
            npc = NPC(self.mongo, name='Test NPC', race='Human', npc_class='Wizard', level=5, alignment='Neutral')
            with patch.object(DnDApiClient, 'get_spell', return_value={'name': 'Fireball', 'level': 3}):
                npc.add_spell('Fireball')
                self.assertEqual(len(npc.spells), 1)
                self.assertEqual(npc.spells[0]['name'], 'Fireball')

    def test_encounter_add_monster(self):
        """Test adding a monster to an encounter."""
        with self.app.app_context():
            encounter = Encounter(self.mongo, title='Battle of Helm', environment='Fortress', party_level=10, difficulty='Hard')
            with patch.object(DnDApiClient, 'get_monster', return_value={'name': 'Orc', 'hit_points': 15}):
                success, _ = encounter.add_monster('Orc')
                assert success
                monster = next((m for m in encounter.monsters if m['name'] == 'Orc'), None)
                assert monster is not None
                assert monster['quantity'] == 1
                assert monster['hit_points'] == 15

    def test_get_monster_success(self):
        """Test getting monster details."""
        with patch.object(DnDApiClient, 'get_monster', return_value={'name': 'Goblin', 'hit_points': 7}):
            dnd_api = DnDApiClient()
            monster = dnd_api.get_monster('Goblin')
            self.assertEqual(monster['name'], 'Goblin')
            self.assertEqual(monster['hit_points'], 7)

if __name__ == '__main__':
    unittest.main()
