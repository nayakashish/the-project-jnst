import pytest
import time
import os
import pytest
import responses
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
# Test 4.1: Test that the response time of the weather endpoint is under 5 seconds
def test_weather_data_load_time(client):
    # Start the timer
    start_time = time.time()

    # Make a request to the weather endpoint
    response = client.get("/api/weather?city=Kelowna")

    # End the timer
    end_time = time.time()

    # Calculate the response time
    response_time = end_time - start_time

    # Assert that the request was successful and the response time is within 5 seconds
    assert response.status_code == 200
    assert response_time <= 5, f"Response time was {response_time} seconds, which exceeds 5 seconds"

# Test 4.2: Tests if system functions as expected with moderate internet connection
@responses.activate
def test_moderate_internet_connection(client):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q=Kelowna&appid={API_KEY}&units=metric"

    # Mock a delayed response (simulate moderate connection with a 2-second delay)
    responses.add(responses.GET, api_url, json={"weather": "mocked data"}, status=200, match_querystring=True, delay=2)

    # Start the timer
    start_time = time.time()

    # Make a request to the endpoint
    response = client.get("/api/weather?city=Kelowna")

    # End the timer
    end_time = time.time()

    # Calculate the response time
    response_time = end_time - start_time

    # Assert that the request was successful and the delay was handled gracefully
    assert response.status_code == 200
    assert response_time >= 2, "The response was too fast, expected a simulated delay"
    assert response_time <= 5, "The response time exceeds acceptable limits for moderate internet"
    assert "mocked data" in response.data.decode()