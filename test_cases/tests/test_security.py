import pytest

# This fixture sets up a testing client for the Flask app
@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True  # Enable testing mode in Flask
    with app.test_client() as client:  # Using Flask's test client to simulate HTTP requests
        yield client

# Test for invalid login attempt
def test_invalid_login(client):
    url = "/login"  # Use relative paths for internal routes
    payload = {"username": "invalidUser", "password": "wrongPassword"}
    response = client.post(url, data=payload)

    # Assert that unauthorized access is prevented
    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials"  # Accessing JSON response directly


# Test to ensure user cannot view dashboard without login
def test_access_protected_resource_without_login(client):
    url = "/dashboard"  # Use relative paths for internal routes
    response = client.get(url)

    # Assert that unauthorized access is prevented
    assert response.status_code == 401
    assert response.json["message"] == "Unauthorized access"
