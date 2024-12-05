#run test with locust -f locustfile.py
# pip install locust
from locust import HttpUser, task, between

class WeatherAppUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a user with delays between actions
    
    @task
    def index(self):
        self.client.get('/index')  # Simulate user hitting the /index page

    @task
    def login(self):
        self.client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
