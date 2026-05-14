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
# Test Get Orders Without Authentication
# User must login first
# ==========================================

def test_get_orders_without_token():

    response = client.get("/orders/")

    # Unauthorized users should not view orders
    assert response.status_code in [401, 403]


# ==========================================
# Test Create Order Without Authentication
# User must login before creating order
# ==========================================

def test_create_order_without_token():

    response = client.post("/orders/")

    # Unauthorized request should fail
    assert response.status_code in [401, 403]


# ==========================================
# Test Get Non Existing Order
# Checks proper handling for missing order
# ==========================================

def test_get_order_by_id_without_token():

    response = client.get("/orders/999999")

    # Possible responses:
    # 401/403 -> unauthorized
    # 404 -> order not found
    assert response.status_code in [401, 403, 404]