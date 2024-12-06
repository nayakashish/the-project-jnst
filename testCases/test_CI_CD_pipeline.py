import pytest
from flask import session
from app import app, weather_app_db

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

