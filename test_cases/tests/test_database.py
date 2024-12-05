import pytest
from database import weather_app_db

def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
#contains random unit tests for database
def db():
    """Fixture to initialize and clean up the database connection."""
    db_instance = weather_app_db()
    yield db_instance
    db_instance.close()

def test_connect(db):
    connection = db.connect()
    assert connection is not None, "Database connection failed."

def test_close_without_connect():
    db_instance = weather_app_db()
    try:
        db_instance.close()
    except Exception:
        pytest.fail("Closing database without connecting raised an exception.")

def test_get_user_info_valid(db):
    db.connect()
    user_info = db.get_user_info(1)  # Replace 1 with a valid user ID in your database
    assert isinstance(user_info, dict), "User info is not a dictionary."
    db.close()
