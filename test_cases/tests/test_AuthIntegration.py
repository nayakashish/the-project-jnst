#test security (security)
import pytest

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_user_registration(client):
    """
    Test that users can create an account if they don't have one already. 
    """
    #Sends a POST request (used when submitting data) to add a location to the dashboard
    response = client.post("/register", json = {"username": "new_user", "password": "secure_pass"}) 
    #Checks if the HTTP request code is 201 (Created), indicating that the user account was succesfully created
    assert response.status_code == 201
    assert b"Account Succesfully Created" in response.data #Confirms that an account was succesfully created. 

def test_user_registration(client):
    """
    Test that the app returns an error for invalid login credentials.
    """
    response = client.post("/login", json = {"username": "fake_user", "password": "wrong_pass"}) 
    ## Checks if the HTTP request code is 401 (Unauthorized), indicating that the login attempt failed due to invalid credentials.
    assert response.status_code == 401
    #Confirms that the error message is returned when invalid credentials are entered. 
    assert b"Invalid username or password." in response.data 

def test_user_registration(client):
    """
    Test that users can log out and end their session
    """
    response = client.post("/logout")
    #Checks if the HTTP request code is 200 (OK), indicating that server succesfully processed the request
    assert response.status_code == 200
    #Confirms that the user has logged out and returns a succesful logout message.
    assert b"You have been logged out" in response.data 



