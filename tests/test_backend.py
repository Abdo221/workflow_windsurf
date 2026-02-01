import pytest
import httpx
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "News Fetcher API"}

def test_fetch_news_success():
    """Test POST /news/fetch with valid category."""
    response = client.post("/news/fetch", json={"category": "science"})
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "attempts" in data
    assert "category" in data
    assert "items" in data
    assert data["category"] == "science"
    assert isinstance(data["attempts"], int)
    assert 1 <= data["attempts"] <= 5
    assert data["status"] in ["FRESH", "CACHED", "PARTIAL"]
    assert isinstance(data["items"], list)

def test_fetch_news_invalid_category():
    """Test POST /news/fetch with invalid category."""
    response = client.post("/news/fetch", json={"category": ""})
    assert response.status_code == 422
    
    response = client.post("/news/fetch", json={"category": "a" * 33})
    assert response.status_code == 422
    
    response = client.post("/news/fetch", json={"category": "invalid@category"})
    assert response.status_code == 422

def test_fetch_news_missing_category():
    """Test POST /news/fetch without category."""
    response = client.post("/news/fetch", json={})
    assert response.status_code == 422
