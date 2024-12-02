import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_retrieve_current_weather(client):
    """
    Test that the app retreives current weather data using the external API.
    """
    response = client.get("/api/weather?city=Kelowna") #Sends GET request to retrieve weather data for Vancouver.
    #Checks if the HTTP request code is 200 (OK), indicating that the server succesfully processed the request
    assert response.status_code == 200 
    assert "temperature" in response.json #Verifies that the JSON response contains a temperature field. 

def test_retrieve_five_day_forecast(client):
    """
    Test that the app retrieves a 5-day weather forecast using the external API
    """ 
    response = client.get("/api/forecast?city=Kelowna") #Sends GET request to retrieve forecast for Vancouver.
    assert response.status_code == 200 
    #Ensures that the forecast field in the response contains 5 days of weather data
    assert len(response.json["forecast"]) == 5 