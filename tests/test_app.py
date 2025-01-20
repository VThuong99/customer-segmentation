from fastapi.testclient import TestClient

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Customer Segmentation API"}

def test_predict_cluster():
    data = {"quantity": 2.0, "unit_price": 3.5, "country": "France"}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "predicted_cluster" in response.json()

def test_predict_cluster_error():
    data = {"quantity": 2.0, "unit_price": "abc", "country": "United Kingdom"}
    response = client.post("/predict", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()