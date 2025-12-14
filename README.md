# Football Players CRUD REST API

A professional REST API built with Flask for managing football player statistics. Includes web UI, JWT authentication, multiple response formats, and comprehensive testing.

## Features

- **CRUD Operations** - Create, Read, Update, Delete players with full validation and error handling
- **JWT Authentication** - Secure protected endpoints with JWT tokens
- **Multiple Formats** - JSON and XML response formats
- **Search Functionality** - Filter players by club or goals
- **Web UI** - Interactive web interface with Create, Edit, Delete, View buttons
- **Comprehensive Testing** - Unit tests covering all operations and edge cases
- **Input Validation** - Type checking, range validation, required field validation
- **Error Handling** - Proper HTTP status codes and descriptive error messages

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Format Support**: JSON, XML
- **Testing**: Python unittest
- **Frontend**: HTML/CSS (responsive web UI)

## Setup
1. Create MySQL database using schema.sql
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `.\venv\Scripts\Activate.ps1`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Running the App
**Important:** Always use the virtual environment Python to run the app (see Setup step 3).

```powershell
# Option 1: Activate venv first, then run normally
.\venv\Scripts\Activate.ps1
python app.py

# Option 2: Run directly with venv Python
.\venv\Scripts\python.exe app.py
```

## Running Tests
```powershell
# Use venv Python for tests
.\venv\Scripts\python.exe test.py
```

## API Endpoints

### Authentication
```
POST /login
```
Generates a JWT token for authenticating protected endpoints.

**Request:** No body required
**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NjU3MDE4ODJ9..."
}
```

### Get All Players
```
GET /players
```
Retrieves all players from the database. Supports filtering and format options.

**Query Parameters:**
- `club` (optional) - Filter players by club name
- `min_goals` (optional) - Filter players with at least this many goals
- `format` (optional) - Response format: `json` or `xml` (default: `json`)

**Response (200):**
```json
{
  "players": [
    {
      "id": 1,
      "name": "Player Name",
      "club": "Club Name",
      "position": "Forward",
      "goals": 25,
      "assists": 10,
      "appearances": 45,
      "created_at": "2024-01-15 10:30:00"
    }
  ]
}
```

### Create Player
```
POST /players
Authorization: Bearer {token}
```
Creates a new player record. Requires valid JWT token.

**Request Body (JSON or XML):**
```json
{
  "id": 100,
  "name": "New Player",
  "club": "Club Name",
  "position": "Midfielder",
  "goals": 5,
  "assists": 3,
  "appearances": 20
}
```
*Note: `id` is optional. If omitted, auto-increment will be used.*

**Response (201):**
```json
{
  "message": "Player created successfully",
  "player": {
    "id": 100,
    "name": "New Player",
    "club": "Club Name",
    "position": "Midfielder",
    "goals": 5,
    "assists": 3,
    "appearances": 20
  }
}
```

**Error (400):** Missing required fields or invalid types
```json
{
  "error": "All fields are required",
  "status": 400
}
```

**Error (401):** Missing or invalid token
```json
{
  "error": "Token is missing!",
  "status": 401
}
```

### Update Player
```
PUT /players/{id}
Authorization: Bearer {token}
```
Updates an existing player record. Requires valid JWT token. All fields are optional for partial updates.

**Request Body (JSON or XML):**
```json
{
  "goals": 30,
  "assists": 12
}
```

**Response (200):**
```json
{
  "message": "Player updated successfully",
  "player": {
    "id": 1,
    "name": "Player Name",
    "club": "Club Name",
    "position": "Forward",
    "goals": 30,
    "assists": 12,
    "appearances": 45
  }
}
```

### Delete Player
```
DELETE /players/{id}
Authorization: Bearer {token}
```
Deletes a player record. Requires valid JWT token.

**Response (200):**
```json
{
  "message": "Player deleted successfully"
}
```

## Usage Examples

### Using cURL

**1. Get Token:**
```bash
curl -X POST http://localhost:5000/login
```

**2. Get All Players:**
```bash
curl http://localhost:5000/players
```

**3. Filter Players by Club:**
```bash
curl "http://localhost:5000/players?club=Manchester%20United"
```

**4. Create Player (with token):**
```bash
curl -X POST http://localhost:5000/players \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cristiano Ronaldo",
    "club": "Al Nassr",
    "position": "Forward",
    "goals": 50,
    "assists": 15,
    "appearances": 80
  }'
```

**5. Update Player (with token):**
```bash
curl -X PUT http://localhost:5000/players/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "goals": 55,
    "assists": 16
  }'
```

**6. Delete Player (with token):**
```bash
curl -X DELETE http://localhost:5000/players/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**7. Get XML Format:**
```bash
curl "http://localhost:5000/players?format=xml"
```

### Using Python
```python
import requests

BASE_URL = "http://localhost:5000"

# Get token
response = requests.post(f"{BASE_URL}/login")
token = response.json()["token"]

# Get all players
response = requests.get(f"{BASE_URL}/players")
print(response.json())

# Create player
headers = {"Authorization": f"Bearer {token}"}
player_data = {
    "name": "Lionel Messi",
    "club": "Inter Miami",
    "position": "Forward",
    "goals": 60,
    "assists": 20,
    "appearances": 90
}
response = requests.post(f"{BASE_URL}/players", json=player_data, headers=headers)
print(response.json())

# Update player
response = requests.put(f"{BASE_URL}/players/1", json={"goals": 65}, headers=headers)
print(response.json())

# Delete player
response = requests.delete(f"{BASE_URL}/players/1", headers=headers)
print(response.json())
```

## Response Formats

### JSON Format (Default)
```json
{
  "players": [
    {
      "id": 1,
      "name": "Player Name",
      "club": "Club Name",
      "position": "Forward",
      "goals": 25,
      "assists": 10,
      "appearances": 45,
      "created_at": "2024-01-15 10:30:00"
    }
  ]
}
```

### XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
  <players>
    <player>
      <id>1</id>
      <name>Player Name</name>
      <club>Club Name</club>
      <position>Forward</position>
      <goals>25</goals>
      <assists>10</assists>
      <appearances>45</appearances>
      <created_at>2024-01-15 10:30:00</created_at>
    </player>
  </players>
</response>
```

## HTTP Status Codes

| Code | Description | Example |
|------|-------------|---------|
| `200` | Success | GET, PUT, DELETE operations successful |
| `201` | Created | Player created successfully |
| `400` | Bad Request | Missing fields, invalid types, out-of-range values |
| `401` | Unauthorized | Missing or invalid JWT token |
| `500` | Server Error | Database connection failure |

## Input Validation

### Field Requirements and Constraints

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `id` | Integer | No | Optional on POST; auto-increment if omitted |
| `name` | String | Yes | Non-empty |
| `club` | String | Yes | Non-empty |
| `position` | String | Yes | One of: Forward, Midfielder, Defender, Goalkeeper |
| `goals` | Integer | Yes | 0-500 |
| `assists` | Integer | Yes | 0-500 |
| `appearances` | Integer | Yes | 0-500 |

**Validation Examples:**
```json
{
  "error": "Goals must be between 0 and 500",
  "status": 400
}
```

## Security

### JWT Authentication
- **Algorithm**: HS256
- **Expiration**: 1 hour from token generation
- **Secret Key**: `football_secret_key`
- **Token Format**: Bearer token in Authorization header

**Example Header:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NjU3MDE4ODJ9...
```

**Protected Endpoints:**
- `POST /players` - Create
- `PUT /players/{id}` - Update
- `DELETE /players/{id}` - Delete

**Public Endpoints:**
- `POST /login` - Get token
- `GET /players` - Read

### Web UI Security
- Session-based authentication
- CSRF protection via form tokens

## Project Structure
```
CSElective-Final-/
├── app.py                 # Main Flask application with all routes
├── auth.py               # JWT token generation and validation
├── config.py             # Database configuration
├── utils.py              # Helper functions (format_response, XML parsing)
├── test.py               # Unit tests (8+ test cases)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── schema.sql            # Database schema (optional reference)
├── templates/            # HTML templates for web UI
│   ├── index.html        # Player list view
│   ├── create.html       # Create player form
│   └── edit.html         # Edit player form
├── scripts/
│   └── run_crud.py       # CRUD demo script (HTTP + test_client modes)
└── venv/                 # Python virtual environment
```
