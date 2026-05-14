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
# Simulates API requests without running server
# ==========================================

client = TestClient(app)


# ==========================================
# Test Get All Products
# Checks that products endpoint is reachable
# ==========================================

def test_get_all_products():

    response = client.get("/products/")

    # 200 -> products returned successfully
    assert response.status_code == 200

    # Response should be a list
    assert isinstance(response.json(), list)


# ==========================================
# Test Get Product That Does Not Exist
# Checks proper 404 handling
# ==========================================

def test_get_non_existing_product():

    response = client.get("/products/999999")

    # 404 -> product not found
    assert response.status_code == 404


# ==========================================
# Test Create Product Without Admin Token
# Normal user / guest should not create products
# ==========================================

def test_create_product_without_token():

    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Product created during testing",
            "price": 100,
            "stock": 10,
            "category_id": 1
        }
    )

    # 401 or 403 -> not authorized
    assert response.status_code in [401, 403]