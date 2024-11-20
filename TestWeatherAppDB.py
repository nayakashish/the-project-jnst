import pytest
import mysql.connector
from weather_app_db import app_DB  # Adjust this import based on your file structure

## For the connection test, the test was created after the main code only in this case
## because we needed to get the connection working at a basic form. 
## all other tests will be written prior to main code except the connection test.

# Test db connection
def test_connect_db():
    app_db = app_DB()
    connection = app_db.connect()
    assert connection is not None  # The connection should be valid and not None
    app_db.close()

