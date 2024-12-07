import pytest
from flask import session
from app import app, weather_app_db

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

#This test checks if the CI pipeline route triggers correctly and returns the expected response with status code 200.
def test_ci_pipeline(client):
    """
    Test that the system runs tests automatically for each new commit.
    """
    response = client.get("/ci/test") # Send a GET request to the /ci/test route
    assert response.status_code == 200 # Verify the status code is 200 (success)
    assert b"Pipeline executed successfully" in response.data # Check if the response contains the expected success message

#This test checks if the /ci/notify route correctly handles a failed build status and returns the expected response.
def test_failed_build_notification(client):
    """
    Test that notifications are sent for failed builds or tests.
    """
    response = client.get("/ci/notify?status=failed") # Send a GET request to the /ci/notify route with a 'failed' status
    assert response.status_code == 200 # Verify the status code is 200 (success)
    assert b"Build failed. Notification sent." in response.data # Check if the response contains the expected failure notification message

#This test verifies that the /deployment/status route returns a successful deployment status response.
def test_deployment(client):
    """
    Test that the application is correctly deployed after the CI pipeline.
    """
    response = client.get("/deployment/status") # Send a GET request to the /deployment/status route
    assert response.status_code == 200 # Verify the status code is 200 (success)
    assert b"Deployment successful" in response.data  # Check if the response contains the expected success message

#This test checks if the /db/connect route indicates a successful connection to the database.
def test_database_connection(client):
    """
    Test that the application successfully connects to the database after deployment.
    """
    response = client.get("/db/connect") # Send a GET request to the /db/connect route
    assert response.status_code == 200 # Verify the status code is 200 (success)
    assert b"Database connection successful" in response.data # Check if the response contains the expected success message

#This test checks if the Flask app has the SECRET_KEY set correctly in the configuration.
def test_environment_variables(client):
    """
    Test that necessary environment variables are set after deployment.
    """
    assert app.config['SECRET_KEY'] == 'my_secret_key'  # Check if SECRET_KEY is set in Flask config