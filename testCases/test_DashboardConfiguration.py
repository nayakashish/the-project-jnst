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

