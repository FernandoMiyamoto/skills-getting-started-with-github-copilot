from fastapi.testclient import TestClient
import pytest
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that root endpoint redirects to index.html"""
    response = client.get("/")
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Test structure of an activity
    activity = next(iter(activities.values()))
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)

def test_signup_for_activity():
    """Test signing up for an activity"""
    # Test successful signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    
    # Test signup for non-existent activity
    response = client.post("/activities/NonExistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # First sign up a test user
    email = "unregister_test@mergington.edu"
    client.post("/activities/Chess Club/signup?email=" + email)
    
    # Test successful unregistration
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Test unregistering when not registered
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
    
    # Test unregistering from non-existent activity
    response = client.delete(f"/activities/NonExistentClub/unregister?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]