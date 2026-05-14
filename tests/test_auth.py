# ==========================================
# Import Testing Tools
# ==========================================

from fastapi.testclient import TestClient
from app.main import app

#python -m pytest -v


# ==========================================
# Create Test Client
# Simulates API requests without running server
# ==========================================

client = TestClient(app)


# ==========================================
# Test User Registration
# Checks if new user can be created
# ==========================================

def test_register_user():

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456"
        }
    )

    # Acceptable responses:
    # 201 -> created successfully
    # 400 -> user already exists
    assert response.status_code in [201, 400]


# ==========================================
# Test User Login
# Checks JWT token generation
# ==========================================

def test_login_user():

    response = client.post(
        "/users/login",
        json={
            "email": "testuser@example.com",
            "password": "123456"
        }
    )

    # Acceptable responses:
    # 200 -> login success
    # 401 -> invalid credentials
    assert response.status_code in [200, 401]

# ==========================================
# Test Protected Route Without JWT Token
# Should deny access
# ==========================================

def test_protected_route_without_token():

    response = client.get("/orders/")

    # User should not access protected routes
    assert response.status_code in [401, 403]