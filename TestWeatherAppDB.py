import pytest
import mysql.connector
from weather_app_db import app_DB  # Adjust this import based on your file structure

## For the connection test, the test was created after the main code only in this case
## because we needed to get the connection working at a basic form. 
## all other tests will be written prior to main code except the connection test.

def test_connect_db():
    app_db = app_DB()
    connection = app_db.connect()
    assert connection is not None  # The connection should be valid and not None
    app_db.close()

def test_get_user_info():
    app_db = app_DB()
    app_db.connect()
    user_info = app_db.get_user_info(user_id=1)
    assert user_info is not None
    expected_result = {
    'id': 1,
    'name': 'Ryan Reynolds',
    'email': 'ryan.reynolds@example.com',
    'theme': 1,
    'temperatureUnit': 'C'
    }
    
    assert user_info == expected_result
    app_db.close()

def test_get_user_info_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    user_info = app_db.get_user_info(999)
    
    out, err = capfd.readouterr()
    assert user_info is None
    assert "No user found with ID 999" in out 

    app_db.close()

def test_add_user():
    app_db = app_DB()
    app_db.connect()
    new_user = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'theme': 2,
        'temperatureUnit': 'F'
    }
    user_id = app_db.add_user(new_user)
    user_info = app_db.get_user_info(user_id)
    assert user_info is not None
    assert user_info['name'] == 'John Doe'
    assert user_info['email'] == 'john.doe@example.com'
    assert user_info['theme'] == 2
    assert user_info['temperatureUnit'] == 'F'
    app_db.close()

def test_add_user_INVALIDName(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': None,  # Invalid name
        'email': 'valid.email@example.com', 
        'theme': 1, 
        'temperatureUnit': 'C'
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is None
    assert "Invalid user data" in out
    app_db.close()

def test_add_user_INVALIDEmail(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': None,  # Invalid email
        'theme': 1,
        'temperatureUnit': 'C'
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is None
    assert "Invalid user data" in out
    app_db.close()

def test_add_user_INVALIDTheme(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': 'valid.email@example.com',
        'theme': 'notanInt',  # Invalid theme
        'temperatureUnit': 'C'
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is None
    assert "Invalid user data" in out
    app_db.close()

def test_add_user_INVALIDTemperatureUnit(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': 'valid.email@example.com',
        'theme': 1,
        'temperatureUnit': 'invalid-unit'  # Invalid temperature unit
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is None
    assert "Invalid user data" in out
    app_db.close()

def test_get_userinfo_byname():
    app_db = app_DB()
    app_db.connect()
    
    user_info = app_db.get_user_info_byname('Ryan Reynolds')
    
    assert user_info is not None
    expected_result = {
        'id': 1,
        'name': 'Ryan Reynolds',
        'email': 'ryan.reynolds@example.com',
        'theme': 1,
        'temperatureUnit': 'C'
    }
    
    assert user_info == expected_result
    app_db.close()

def test_get_userinfo_byname_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    user_info = app_db.get_user_info_byname('Nonexistent User')
    
    out, err = capfd.readouterr()
    assert user_info is None
    assert "No user found with name Nonexistent User" in out
    app_db.close()

def test_update_user_info():
    app_db = app_DB()
    app_db.connect()
    updated_info = {
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'theme': 3,
        'temperatureUnit': 'C'
    }
    app_db.update_user_info(1, updated_info)
    user_info = app_db.get_user_info(1)
    assert user_info is not None
    assert user_info['name'] == 'Jane Doe'
    assert user_info['email'] == 'jane.doe@example.com'
    assert user_info['theme'] == 3
    assert user_info['temperatureUnit'] == 'C'
    app_db.close()

def test_update_user_info_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    updated_info = {
        'name': 'Invalid User',
        'email': 'invalid.user@example.com',
        'theme': 4,
        'temperatureUnit': 'F'
    }
    app_db.update_user_info(999, updated_info)
    
    out, err = capfd.readouterr()
    assert "No user found with ID 999" in out
    app_db.close()

def test_delete_user():
    app_db = app_DB()
    app_db.connect()
    app_db.delete_user(1)
    user_info = app_db.get_user_info(1)
    assert user_info is None
    app_db.close()

def test_delete_user_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    app_db.delete_user(999)
    
    out, err = capfd.readouterr()
    assert "No user found with ID 999" in out
    app_db.close()