#test backend (maintainabilty)
import pytest
from weather_app_db import app_DB

@pytest.fixture
def client():
    """Fixture to initialize the Flask test client."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirect to /index

def test_index_route(client):
    response = client.get('/index')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Replace 'Welcome' with known content

def test_login_success(client, mocker):
    # Use mocker to replace the 'get_userid' and 'get_user_info' methods from 'weather_app_db' with predefined outputs.
    # This simulates database responses without requiring an actual database connection.

    mocker.patch('weather_app_db.get_userid', return_value=1) #mocker is a test instance of the app.py
    mocker.patch('weather_app_db.get_user_info', return_value={'name': 'testuser', 'password': 'testpassword'})
    
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302  # Redirect to /index
    assert b"You've been logged in successfully!" in response.data


