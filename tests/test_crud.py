# ==========================================
# CRUD Endpoint API Tests
# Tests Create, Read, Update, Delete routes
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
# Test Read Products
# ==========================================

def test_read_products():

    response = client.get("/products/")

    assert response.status_code == 200


# ==========================================
# Test Create Product Without Admin
# ==========================================

def test_create_product():

    response = client.post(
        "/products/",
        json={
            "name": "CRUD Test Product",
            "description": "Testing create endpoint",
            "price": 100,
            "stock": 5,
            "category_id": 1
        }
    )

    assert response.status_code in [401, 403]


# ==========================================
# Test Update Product Without Admin
# ==========================================

def test_update_product():

    response = client.put(
        "/products/1",
        json={
            "name": "Updated Product",
            "description": "Updated description",
            "price": 200,
            "stock": 10,
            "category_id": 1
        }
    )

    assert response.status_code in [401, 403]


# ==========================================
# Test Delete Product Without Admin
# ==========================================

def test_delete_product():

    response = client.delete("/products/1")

    assert response.status_code in [401, 403]