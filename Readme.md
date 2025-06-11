# Simple Investment Tracker API

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation and Setup

1. Clone the repository or copy the project files.

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirement.txt
   ```

4. Run database migrations (using SQLite by default):

   ```bash
   python manage.py migrate
   ```

5. (Optional) Load sample data fixture for testing:

   ```bash
   python manage.py loaddata sample_data.json
   ```

6. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

API runs at: `http://localhost:8000/`

---

## API Endpoints

### User Login / Obtain JWT Token

- **URL:** `/api/auth/login/`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "username": "user",
    "password": "securepassword"
  }
  ```
- **Response:**
  ```json
  {
    "access": "<jwt-access-token>",
    "refresh": "<jwt-refresh-token>"
  }
  ```

### Create Investment

- **URL:** `/api/investments/`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "asset_name": "TESLA",
    "amount_invested": 1200,
    "purchase_date": "2025-01-15",
    "current_value": 1300,
    "is_active": true
  }
  ```
- **Response:** Investment creation confirmation or errors.

### List User Investments

- **URL:** `/api/investments/`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** List of investments for the authenticated user.

### Portfolio Summary

- **URL:** `/api/investments/summary/`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:** JSON summary of total invested, current portfolio value, profit/loss, active investments count, best/worst performing assets.

---

## Sample curl Commands

```bash
# Login and get JWT token
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'

# Create an investment (replace <ACCESS_TOKEN>)
curl -X POST http://localhost:8000/api/investments/ \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
-H "Content-Type: application/json" \
-d '{"asset_name": "TSLA", "amount_invested": 1500, "purchase_date": "2025-03-20", "current_value": 1600, "is_active": true}'

# Fetch portfolio summary
curl -X GET http://localhost:8000/api/investments/summary/ \
-H "Authorization: Bearer <ACCESS_TOKEN>"
```

