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
        'temperatureUnit': 'F',
        'password': "mystrongpass"
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
        'temperatureUnit': 'C',
        'password': "mystrongpass"
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is False
    assert "Invalid" in out
    app_db.close()

def test_add_user_INVALIDEmail(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': None,  # Invalid email
        'theme': 1,
        'temperatureUnit': 'C',
        'password': "mystrongpass"
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is False
    assert "Invalid" in out
    app_db.close()

def test_add_user_INVALIDTheme(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': 'valid.email@example.com',
        'theme': 'notanInt',  # Invalid theme
        'temperatureUnit': 'C',
        'password': "mystrongpass"
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is False
    assert "Invalid" in out
    app_db.close()

def test_add_user_INVALIDTemperatureUnit(capfd):
    app_db = app_DB()
    app_db.connect()
    invalid_user = {
        'name': 'Valid Name',
        'email': 'valid.email@example.com',
        'theme': 1,
        'temperatureUnit': 'invalid-unit',  # Invalid temperature unit
        'password': "mystrongpass"
    }
    user_id = app_db.add_user(invalid_user)
    
    out, err = capfd.readouterr()
    assert user_id is False
    assert "Invalid" in out
    app_db.close()

def test_get_userid():
    app_db = app_DB()
    app_db.connect()
    
    user_id = app_db.get_userid('Ryan Reynolds')
    
    assert user_id is not None
    assert user_id == 1
    app_db.close()

def test_get_userid_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    user_id = app_db.get_userid('Nonexistent User')
    
    out, err = capfd.readouterr()
    assert user_id is False
    assert "No user found with name Nonexistent User" in out
    app_db.close()

def test_update_user_info():
    app_db = app_DB()
    app_db.connect()
    
    # Add a temporary user
    temp_user = {
        'name': 'Temp User',
        'email': 'temp.user@example.com',
        'theme': 1,
        'temperatureUnit': 'C',
        'password': "temppass"
    }
    user_id = app_db.add_user(temp_user)
    
    # Update the temporary user's information
    updated_info = {
        'name': 'Updated Temp User',
        'email': 'updated.temp.user@example.com',
        'theme': 2,
        'temperatureUnit': 'F'
    }
    app_db.update_user_info(user_id, **updated_info)
    
    # Retrieve and check the updated information
    user_info = app_db.get_user_info(user_id)
    assert user_info is not None
    assert user_info['name'] == 'Updated Temp User'
    assert user_info['email'] == 'updated.temp.user@example.com'
    assert user_info['theme'] == 2
    assert user_info['temperatureUnit'] == 'F'
    
    app_db.delete_user(user_id)
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
    app_db.update_user_info(999, **updated_info)
    
    out, err = capfd.readouterr()
    assert "No user found with ID 999" in out
    app_db.close()

def test_delete_user():
    app_db = app_DB()
    app_db.connect()
    delete_id = app_db.get_userid("John Doe")
    ret = app_db.delete_user(delete_id)
    assert ret == delete_id
    user_info = app_db.get_user_info(delete_id)
    assert user_info is None
    app_db.close()

def test_delete_user_INVALID(capfd):
    app_db = app_DB()
    app_db.connect()
    ret = app_db.delete_user(999)
    assert ret is False
    out, err = capfd.readouterr()
    assert "No user found with ID 999" in out
    app_db.close()

def test_add_location():
    app_db = app_DB()
    app_db.connect()
    location_id = app_db.add_location("Kelowna")
    assert location_id is not None #if it failed, location id would be false;
    app_db.close()

def test_add_location_duplicate():
    app_db = app_DB()
    app_db.connect()
    
    location_id_1 = app_db.add_location("Redcliff")
    assert location_id_1 is not None
    
    location_id_2 = app_db.add_location("Redcliff")
    assert location_id_2 is not None
    
    assert location_id_1 == location_id_2 #the locations should be same as the second one will return existing location found in db instead of creating new one
    
    app_db.close()