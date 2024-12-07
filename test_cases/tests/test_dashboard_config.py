#test dashboard (usability)
import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_location_to_dashboard(client):
    """
    Test that users can add a new location to their dashboard. 
    """
    #Sends a POST request (used when submitting data) to add a location to the dashboard
    response = client.post("/dashboard/add", json = {"location": "Vancouver"}) 
    #Checks if the HTTP request code is 200 (OK), indicating that the server succesfully processed the request
    assert response.status_code == 200 
    assert b"Vancouver added to your dashboard" in response.data #Confirms that the location was added.

def test_remove_location_from_dashboard(client):
    """
    Test that users can remove a location from their dashboard. 
    """
    response = client.post("/dashboard/adremoved", json = {"location": "Vancouver"}) 
    assert response.status_code == 200 
    assert b"Vancouver was removed from your dashboard" in response.data #Confirms that the location was removed.

def test_save_dashboard_preferences(client):
    """
    Tests that dahshboard preferences are saved after changes
    """
    response = client.post("/dashboard/preferences", json = {"theme": "dark", "units": "imperial"}) 
    assert response.status_code == 200 
    #Confirms that the dashboard preferences are sucessfully updated.
    assert b"Dashboard preferences updated succesfully" in response.data 