The weather_app_db.py file defines a class app_DB that handles database operations for a weather application. \ 

A list of functions in the class:
 - connect()
 - close()
 - get_user_info(user_id)
   - Returns user_info as obj or none.
 - get_userid(user_name)
   - Returns userId or false.
 - add_user(user_info)
   - Returns newly added userId or false.
 - delete_user(user_id)
   - Returns deleted userId or false.
 - update_user_info(user_id, updated_data)
   - Example how to use function: \
`user_id = 1 (The ID of the user you want to update)` \
`update_data = {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'theme': 'dark',
    'temperatureUnit': 'Celsius'
}` \
Then call the update_user_info method with the user_id and the update_data: \
`result = db_instance.update_user_info(user_id, **update_data)`
 - get_locationName(location_id)
   - Returns location name or false.
 - get_locationID(location_name)
   - Returns locationId or false;
 - add_location(location_name)
   - Returns location_id or false.
 - add_dashboardLocation(user_id, location_id)
   - Returns true or false.
 - get_dashboardLocations(user_id)
   - Returns list of locations or false.
 - delete_dashboardLocation(user_id, location_id)
   - Returns true or false.



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

Also useful is that main weather_app_db.py file has a function at the bottom that can be run by team members for testing out functions and getting familiar with the database.  g