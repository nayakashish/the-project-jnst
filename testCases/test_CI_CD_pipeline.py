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