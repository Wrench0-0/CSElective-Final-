import unittest
import json
from app import app
from auth import generate_token

class PlayerApiTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.token = generate_token()

    def test_get_players(self):
        res = self.client.get('/players')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_xml_output(self):
        res = self.client.get('/players?format=xml')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<?xml', res.data)

    def test_create_no_token(self):
        res = self.client.post('/players', json={})
        self.assertEqual(res.status_code, 401)

    def test_create_with_token(self):
        res = self.client.post('/players',
            json={
                'name': 'Test Player',
                'club': 'Test FC',
                'position': 'Forward',
                'goals': 5,
                'assists': 2,
                'appearances': 10
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Player')
        self.player_id = data['id']

    def test_update_with_token(self):
        # First create a player
        res = self.client.post('/players',
            json={
                'name': 'Update Test',
                'club': 'Test FC',
                'position': 'Midfielder',
                'goals': 3,
                'assists': 5,
                'appearances': 8
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        player_id = json.loads(res.data)['id']
        
        # Update the player
        res = self.client.put(f'/players/{player_id}',
            json={'goals': 10, 'assists': 8},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['goals'], 10)
        self.assertEqual(data['assists'], 8)

    def test_delete_with_token(self):
        # First create a player
        res = self.client.post('/players',
            json={
                'name': 'Delete Test',
                'club': 'Test FC',
                'position': 'Defender',
                'goals': 1,
                'assists': 1,
                'appearances': 5
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        player_id = json.loads(res.data)['id']
        
        # Delete the player
        res = self.client.delete(f'/players/{player_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('message', data)

    def test_delete_no_token(self):
        res = self.client.delete('/players/1')
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
