# CSElective-Final-
# Football Players CRUD REST API

## Features
- Flask + MySQL REST API
- CRUD operations
- JWT Authentication
- JSON & XML formatting
- Search by club or goals
- Unit testing

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

## Authentication
POST /login → returns JWT token

## API Endpoints
- GET /players
- POST /players (JWT)
- PUT /players/{id} (JWT)
- DELETE /players/{id} (JWT)

## Format
?format=json or ?format=xml
