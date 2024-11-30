import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_view_weather_on_open(client):
    """
    Test that the app allows users to view weather when connected to a network.
    """
    response = client.get("/") #Sends a GET request to the route ("/") of the app
    assert response.status_code == 200 #Checks if the HTTP request code is 200 (OK), indicating that server succesfully processed the request
    assert b"Current Weather" in response.data #Verifies that the response contains "Current Weather" text