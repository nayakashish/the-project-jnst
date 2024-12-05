import pytest
from weather_app_db import app_DB

@pytest.fixture
def db():
    """Fixture to initialize and clean up the database connection."""
    weather_app_db = app_DB()
    yield weather_app_db
    weather_app_db.close()

@pytest.fixture
def client():
    """Fixture to initialize the Flask test client."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_connect(db):
    """Test that the database connection is successful."""
    connection = db.connect()
    assert connection is not None, "Database connection failed."

def test_close_should_succeed_without_connection():
    """Test that closing the database connection without connecting does not raise an error."""
    weather_app_db = app_DB()
    try:
        weather_app_db.close()
        assert True
    except Exception as e:
        pytest.fail(f"Closing database without connecting raised an exception: {e}")

def test_get_user_info_valid(db):
    """Test retrieving valid user info from the database."""
    db.connect()
    user_info = db.get_user_info(1)  # Replace 1 with a valid user ID in your database
    assert isinstance(user_info, dict), "User info is not a dictionary."

def test_get_user_info_invalid(db):
    """Test retrieving user info for a non-existent user ID."""
    db.connect()
    user_info = db.get_user_info(9999)  # Assuming 9999 is an invalid user ID
    assert user_info is None, "User info should be None for an invalid user ID."
