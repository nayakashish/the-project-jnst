import os
import pytest
import responses
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# This fixture sets up a testing client for the Flask app
# Mock the API
@responses.activate

@pytest.fixture # test feature for flask app
def client():
    from app import app
    with app.test_client() as client:
        yield client

def test_api_error_handling(client):
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