import pytest
from fastapi import HTTPException
from src.app import activities

def test_activities_data_structure():
    """Test the structure of the activities data"""
    for name, activity in activities.items():
        assert isinstance(name, str)
        assert isinstance(activity, dict)
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
        assert all(isinstance(email, str) for email in activity["participants"])

def test_activities_constraints():
    """Test that activities data meets business constraints"""
    for name, activity in activities.items():
        # Activity name should not be empty
        assert len(name) > 0
        
        # Description should not be empty
        assert len(activity["description"]) > 0
        
        # Schedule should not be empty
        assert len(activity["schedule"]) > 0
        
        # Maximum participants should be positive
        assert activity["max_participants"] > 0
        
        # Current participants should not exceed maximum
        assert len(activity["participants"]) <= activity["max_participants"]
        
        # Email addresses should be from mergington.edu domain
        for email in activity["participants"]:
            assert email.endswith("@mergington.edu")

def test_unique_participants():
    """Test that each participant is registered only once per activity"""
    for activity in activities.values():
        # Convert list to set and back to list to check for duplicates
        unique_participants = list(set(activity["participants"]))
        assert len(unique_participants) == len(activity["participants"])