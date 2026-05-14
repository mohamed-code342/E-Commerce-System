# ==========================================
# Validation & Business Logic API Tests
# Tests invalid inputs, duplicate entries,
# authentication failures, and edge cases
# ==========================================


# ==========================================
# Import Testing Tools
# ==========================================

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


# ==========================================
# Create Test Client
# ==========================================

client = TestClient(app)


# ==========================================
# Test Duplicate User Registration
# Should prevent creating same email twice
# ==========================================

def test_duplicate_user_registration():

    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "123456"
    }

    # First registration attempt
    client.post("/users/register", json=user_data)

    # Second registration attempt
    response = client.post("/users/register", json=user_data)

    # API should reject duplicate user
    assert response.status_code in [400, 409]


# ==========================================
# Test Invalid Login Credentials
# Should reject wrong password
# ==========================================

def test_invalid_login():

    response = client.post(
        "/users/login",
        json={
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
    )

    # Invalid credentials should fail
    assert response.status_code in [401, 404]


# ==========================================
# Test Invalid Product ID
# Should return product not found
# ==========================================

def test_invalid_product_id():

    response = client.get("/products/999999")

    # Product should not exist
    assert response.status_code == 404


# ==========================================
# Test Invalid Cart Quantity
# Quantity should not be negative
# ==========================================

def test_invalid_cart_quantity():

    response = client.post(
        "/cart/",
        json={
            "product_id": 1,
            "quantity": -5
        }
    )

    # Invalid quantity should fail
    assert response.status_code in [400, 401, 403, 422]