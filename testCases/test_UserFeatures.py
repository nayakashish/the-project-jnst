import pytest
from flask import session
from app import app, weather_app_db

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(client):
    with client.session_transaction() as sess:
        sess['userLoggedin'] = True
        sess['userName'] = 'testuser'
        sess['db_connection_failed'] = False

    # Mock the database connection and methods
    weather_app_db.connect = lambda: None
    weather_app_db.close = lambda: None
    weather_app_db.get_dashboardLocations = lambda user_id: [
        {'name': 'New York'},
        {'name': 'Los Angeles'},
        {'name': 'Chicago'}
    ]
    weather_app_db.get_userid = lambda username: 1

    return client


def test_view_weather_on_open(client):
    """
    Test that the app allows users to view weather when connected to a network.
    """
    response = client.get("/") #Sends a GET request to the route ("/") of the app
    assert response.status_code == 200 #Checks if the HTTP request code is 200 (OK), indicating that server succesfully processed the request
    assert b"Current Weather" in response.data #Verifies that the response contains "Current Weather" text

def test_view_five_day_forecast(client):
    """
    Test that the app provides a 5 day weather forecast.
    """
    response = client.get("/") #Sends a GET request to the "/forecast" route
    assert response.status_code == 200
    assert b"5-Day Forecast" in response.data #Verifies that the response contains "5-Day Forecast" text

def test_search_location(client):
    """
    Test that the app allows searching for location by name.
    """
    response = client.get("/weather?city=Kelowna") #Sends a GET request with a city parameter
    assert response.status_code == 200
    assert b"Kelowna" in response.data #Verifies that the response includes the searched city name

# removed duplicate test test_userLogin

def test_successful_login(client):
    response = client.post("/login", data={"username": "Ryan Reynolds", "password": "ryanPass"})
    assert response.status_code == 302  # Redirect to index
    with client.session_transaction() as sess:
        assert sess['userLoggedin'] == True
        assert sess['userName'] == "Ryan Reynolds"  # Replace with actual expected name

def test_invalid_username(client):
    response = client.post("/login", data={"username": "invalid_user", "password": "ryanPass"})
    assert response.status_code == 200  # Stay on login page
    assert b"Invalid username." in response.data
    with client.session_transaction() as sess:
        assert sess['userLoggedin'] == False

def test_invalid_password(client):
    response = client.post("/login", data={"username": "Ryan Reynolds", "password": "invalid_password"})
    assert response.status_code == 200  # Stay on login page
    assert b"Invalid password." in response.data
    with client.session_transaction() as sess:
        assert sess['userLoggedin'] == False

#No need for tests for empty fields as the form has required fields

def test_logout(client):
    # First, log in the user
    response = client.post("/login", data={"username": "Ryan Reynolds", "password": "ryanPass"})

    # Then, log out the user
    response = client.get("/logout")
    assert response.status_code == 302  # Redirect to index
    # assert b"You've been successfully logged out!" in response.data # Commented out because the response is a redirect, the text is not seen in reponse
    with client.session_transaction() as sess:
        assert 'userLoggedin' not in sess
        assert 'userName' not in sess

def test_logged_in_user_sees_saved_locations_weather(logged_in_client):
    """
    Test that a logged-in user sees the saved locations' weather.
    """
    response = logged_in_client.get('/index')
    assert response.status_code == 200
    #assert b'New York' in response.data #This was removed since the saved locations will show locations 2,3,4 and main will show 1
    assert b'Los Angeles' in response.data
    assert b'Chicago' in response.data

def test_non_logged_in_user_sees_default_locations(client):
    """
    Test that a non-logged-in user sees the default locations' weather.
    """
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Example Location' in response.data
    assert b'Please login to save locations' in response.data

def test_logged_in_user_with_no_locations(logged_in_client):
    """
    Test that a logged-in user with no saved locations sees an appropriate message.
    """
    # Mock the database method to return an empty list for locations
    weather_app_db.get_dashboardLocations = lambda user_id: []

    response = logged_in_client.get('/index')
    assert response.status_code == 200
    assert b'No saved locations' in response.data
    assert b'Follow the link below to add locations!' in response.data

def test_shared_dashboard(logged_in_client):
    """
    Test that the shared dashboard displays the correct locations for the given dash_id.
    """
    response = logged_in_client.get('/shared_dashboard?dash_1') #enter the url for a shared dash for the logged_in_client
    assert response.status_code == 200
    assert b'New York' in response.data
    assert b'Los Angeles' in response.data
    assert b'Chicago' in response.data
    
def test_non_logged_in_user_cannot_access_shared_dashboard(client):
    """
    Test that a non-logged-in user cannot access the shared dashboard.
    """
    response = client.get('/shared_dashboard/dash_1')
    assert response.status_code == 302  # Redirect to login page
