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
# Test Access Cart Without Authentication
# User must login first
# ==========================================

def test_get_cart_without_token():

    response = client.get("/cart/")

    # Unauthorized access should fail
    assert response.status_code in [401, 403]


# ==========================================
# Test Add Item To Cart Without Token
# ==========================================

def test_add_to_cart_without_token():

    response = client.post(
        "/cart/",
        json={
            "product_id": 1,
            "quantity": 2
        }
    )

    # User should not add items without login
    assert response.status_code in [401, 403]


# ==========================================
# Test Remove Item From Cart Without Token
# ==========================================

def test_remove_cart_item_without_token():

    response = client.delete("/cart/1")

    # Unauthorized request should fail
    assert response.status_code in [401, 403]