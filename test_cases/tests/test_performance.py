import pytest
import time

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
