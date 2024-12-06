import pytest
from flask import session
from app import app, weather_app_db

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_ci_pipeline(client):
    """
    Test that the system runs tests automatically for each new commit.
    """
    response = client.get("/ci/test")  # Mock endpoint to trigger the test pipeline.
    assert response.status_code == 200  # Ensure the pipeline starts without errors.
    assert b"Pipeline executed successfully" in response.data  # Confirm the pipeline ran.

def test_failed_build_notification(client):
    """
    Test that notifications are sent for failed builds or tests.
    """
    response = client.get("/ci/notify?status=failed")  # Mock a failed pipeline notification.
    assert response.status_code == 200  # Check if the notification request succeeds.
    assert b"Build failed. Notification sent." in response.data  # Confirm the failure was notified.

# Test for the application deployment after CI pipeline
def test_deployment(client):
    """
    Test that the application is correctly deployed after the CI pipeline.
    """
    response = client.get("/deployment/status")  # Access the endpoint for deployment status
    assert response.status_code == 200  # Ensure the status is returned successfully
    assert b"Deployment successful" in response.data  # Confirm deployment success

# Test for the database connection after deployment
def test_database_connection(client):
    """
    Test that the application successfully connects to the database after deployment.
    """
    response = client.get("/db/connect")  # Mock the database connection check
    assert response.status_code == 200  # Ensure the DB connection check is successful
    assert b"Database connection successful" in response.data  # Confirm the database is reachable

def test_environment_variables(client):
    """
    Test that necessary environment variables are set after deployment.
    """
    assert app.secret_key == 'my_secret_key'  # Check if SECRET_KEY matches the expected value