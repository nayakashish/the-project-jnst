import os
import pytest
import responses
from dotenv import load_dotenv

# This fixture sets up a testing client for the Flask app
@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True  # Enable testing mode in Flask
    with app.test_client() as client:  # Using Flask's test client to simulate HTTP requests
        yield client

# Load environment variables from .env file
load_dotenv()

# Mock the API
@responses.activate

def test_api_error_handling(client):
    """
    Test that the api handles errors as intended.
    """
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    # Simulate a server error
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q=kelowna&appid={API_KEY}&units=metric" #test url
    responses.add(responses.GET, api_url, status=503)

    # Trigger the request in your app
    response = client.get("/api/weather?city=Kelowna")  # Your app's endpoint that calls the API

    # Check that the app handles the error gracefully
    assert response.status_code == 200  # Your app should respond normally to the user
    assert "Service is temporarily unavailable" in response.data.decode()  # Error message displayed

    # Verify retry logic
    assert len(responses.calls) == 1  # Ensure the app didn't retry automatically without user input

   
def test_session_data_persistence(client):
    """
    Test if system maintains session data for duration of user interaction 
    """
    # Step 1: Log in and set session data
    login_payload = {"username": "Ryan Reynolds", "password": "ryanPass"} # testing with these credentials
    response = client.post("/login", data=login_payload)

    # Assert successful login and session setup
    assert response.status_code == 200
    assert "Welcome testuser" in response.data.decode()

    # Step 2: Access dashboard route (only available to logged in users) to verify session persistence
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Hello testuser" in response.data.decode()  # Example of session data usage

def test_session_timeout(client):
    """
    Test if system logs out user on session timeout 
    """
    # Step 1: Log in and set session data
    login_payload = {"username": "Ryan Reynolds", "password": "ryanPass"}
    response = client.post("/login", data=login_payload)

    # Assert successful login and session setup
    assert response.status_code == 200
    assert "Welcome testuser" in response.data.decode()

    # Step 2: Log out the user by simulating session expiration (Flask does not handle timeouts by default)
    with client.session_transaction() as session:
        session.clear()  # Manually clear session to simulate timeout

    # Step 3: Attempt to access a dashboard route after logging out
    response = client.get("/dashboard")
    assert response.status_code == 401  # Unauthorized
    assert "Session expired, please log in again" in response.data.decode()