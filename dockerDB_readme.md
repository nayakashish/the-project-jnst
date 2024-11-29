This file will soon be updated to reflect how the database interacts with the rest of the application. As well as how to setup the environment.

### Useful commands:
```docker compose up -d``` \
```docker exec -it cosc310-jnst-db bash``` \
```mysql -u root -p``` \
Pass: ```jnstRoot``` \
```show databases;``` \

### Dependencies:
```pip install pytest``` \
```pip install mysql-connector-python ```

1. Have docker desktop running in the background
2. In the terminal run `docker-compose up` (add -d to run in detached mode... if you do not want to see the logs.)
3. Docker should create/start the database. 
4. In the terminal run `pytest TestWeatherAppDB.py`
5. The test should all run and pass successfully. 
6. To stop the docker container you can run `docker-compose down` or pause it in the desktop application.

Also useful is that main weather_app_db.py file has a function at the bottom that can be run by team members for testing out functions and getting familiar with the database.  