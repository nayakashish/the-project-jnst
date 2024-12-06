import pytest
from flask import session
import os
from app import app, weather_app_db

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ci_pipeline(client):
    response = client.get("/ci/test")
    assert response.status_code == 200
    assert b"Pipeline executed successfully" in response.data

def test_failed_build_notification(client):
    response = client.get("/ci/notify?status=failed")
    assert response.status_code == 200
    assert b"Build failed. Notification sent." in response.data

def test_deployment(client):
    response = client.get("/deployment/status")
    assert response.status_code == 200
    assert b"Deployment successful" in response.data

def test_database_connection(client):
    response = client.get("/db/connect")
    assert response.status_code == 200
    assert b"Database connection successful" in response.data

def test_environment_variables(client):
    """
    Test that necessary environment variables are set after deployment.
    """
    assert app.config['SECRET_KEY'] == 'my_secret_key'  # Check if SECRET_KEY is set in Flask config