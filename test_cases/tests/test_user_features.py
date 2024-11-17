import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_view_weather_on_open(client):
    """
    Test that the app allows users to iew wather when connected to a network.
    """
    response = client.get("/") #Sends a GET request to the route ("/") of the app
    assert response.status_code == 200 #Checks if the HTTP request code is 200 (OK), indicating that erver succesfully processed the request
    assert b"Current Weather" in response.data #Verifies that the response contains "Current Weather" text

def test_view_five_day_forecast(client):
    """
    Test that the app provides a 5 day forecast
    """
    response = client.get("/") #Sends a GET request to the "/forecast" route
    assert response.status_code == 200
    assert b"5-Day Forecast" in response.data #Verifies that the response contains "5-Day Forecast" text

def test_search_location(client):
    """
    Test that the app allows searching for location by name
    """
    response = client.get("/weather?city=Kelowna") #Sends a GET request with a city parameter
    assert response.status_code == 200
    assert b"Kelowna" in response.data #Verifies that the response includes the searched city name

def test_user_login(client):
    """
    Test that users must log in to access specific features
    """
    #Sends a POST (used when submitting data) request to "/login" with mock credentials
    response = client.get("/login", json = {"username": "test_user", "password": "test_pass"}) 
    assert response.status_code == 200
    assert b"Welcome test_user" in response.data #Verify that the response includes a welcome message