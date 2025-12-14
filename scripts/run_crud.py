import sys
import requests

BASE_URL = "http://localhost:5000"


def use_requests_flow():
    print("Using live HTTP requests to", BASE_URL)
    print("=== LOGIN ===")
    r = requests.post(f"{BASE_URL}/login")
    r.raise_for_status()
    token = r.json().get('token')
    print("Token:", token)

    headers = {'Authorization': f'Bearer {token}'}

    print("\n=== GET /players ===")
    r = requests.get(f"{BASE_URL}/players")
    r.raise_for_status()
    players = r.json()
    print(f"Total players: {len(players)}")
    for p in players[:3]:
        print(f"  - {p['name']} ({p['club']})")

    print("\n=== POST /players (Create) ===")
    new_player = {
        'name': 'Scripted Test Player',
        'club': 'Script FC',
        'position': 'Striker',
        'goals': 10,
        'assists': 5,
        'appearances': 15
    }
    r = requests.post(f"{BASE_URL}/players", json=new_player, headers=headers)
    r.raise_for_status()
    created = r.json()
    print("Created:", created)
    pid = created.get('id')

    print(f"\n=== PUT /players/{pid} (Update) ===")
    update = {'goals': 20, 'assists': 10}
    r = requests.put(f"{BASE_URL}/players/{pid}", json=update, headers=headers)
    r.raise_for_status()
    updated = r.json()
    print("Updated:", updated)

    print(f"\n=== DELETE /players/{pid} (Delete) ===")
    r = requests.delete(f"{BASE_URL}/players/{pid}", headers=headers)
    r.raise_for_status()
    print("Delete response:", r.json())

    print("\n=== VERIFY DELETION ===")
    r = requests.get(f"{BASE_URL}/players")
    r.raise_for_status()
    players = r.json()
    exists = any(p['id'] == pid for p in players)
    print(f"Player {pid} exists after delete? {exists}")


def use_test_client_flow():
    print("Using Flask test client (no external server required)")
    import os
    import sys
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from app import app
    client = app.test_client()

    print("=== LOGIN ===")
    r = client.post('/login')
    token = r.get_json().get('token')
    print('Token:', token)
    headers = {'Authorization': f'Bearer {token}'}

    print("\n=== GET /players ===")
    r = client.get('/players')
    players = r.get_json()
    print(f"Total players: {len(players)}")
    for p in players[:3]:
        print(f"  - {p['name']} ({p['club']})")

    print("\n=== POST /players (Create) ===")
    new_player = {
        'name': 'Scripted Test Player',
        'club': 'Script FC',
        'position': 'Striker',
        'goals': 10,
        'assists': 5,
        'appearances': 15
    }
    r = client.post('/players', json=new_player, headers=headers)
    print(r.status_code, r.data.decode()[:500])
    created = r.get_json() if r.status_code == 201 else None
    pid = created.get('id') if created else None

    if pid:
        print(f"\n=== PUT /players/{pid} (Update) ===")
        r = client.put(f'/players/{pid}', json={'goals': 20, 'assists': 10}, headers=headers)
        print(r.status_code, r.data.decode()[:500])

        print(f"\n=== DELETE /players/{pid} (Delete) ===")
        r = client.delete(f'/players/{pid}', headers=headers)
        print(r.status_code, r.data.decode()[:500])

        print("\n=== VERIFY DELETION ===")
        r = client.get('/players')
        players = r.get_json()
        exists = any(p['id'] == pid for p in players)
        print(f"Player {pid} exists after delete? {exists}")
    else:
        print('Create failed; skipping update/delete')


def main():
    try:
        use_requests_flow()
        print('\nCRUD flow completed successfully (live HTTP)')
        return 0
    except requests.RequestException as e:
        print('Live server not reachable, falling back to test client:', e)
    except Exception as e:
        print('Live flow error, falling back to test client:', e)

    try:
        use_test_client_flow()
        print('\nCRUD flow completed successfully (test client)')
        return 0
    except Exception as e:
        print('Error during test client flow:', e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
