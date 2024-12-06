# this is the server
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 
import os, sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from dotenv import load_dotenv
from weather_app_db import app_DB
# Get current time and date in PST
from datetime import datetime, timedelta, timezone
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# OpenWeather API key (To be added)
API_KEY = os.getenv("API_KEY")
weather_app_db = app_DB()

# Reusable function to get weather data
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return None  # or maybe change to raise an exception if needed?

    return response.json()

@app.route("/")
def home():
    session.clear()
    db_connection_failed = session.get('db_connection_failed', True)
    print("SERVER IS RUNNING")
    if not weather_app_db.connect():
        print("Error: Failed to connect to the database.")
        session['db_connection_failed'] = True
    else:
        print("Connected to the database!")
        session['db_connection_failed'] = False
        weather_app_db.close()
        print("Closed connection to database")
   
    return redirect(url_for('index'))
    # return render_template("index.html", db_connection_failed= session['db_connection_failed'])

@app.route('/index')
def index():
    db_connection_failed = session.get('db_connection_failed', True)
    userLoggedin = session.get('userLoggedin', False)
    userName = session.get('userName', None)

    if userLoggedin: #if user is logged in mini dashboard shows
        weather_app_db.connect()
        locations = weather_app_db.get_dashboardLocations(weather_app_db.get_userid(userName)) #get locations from db
        if locations:
            locations = locations[1:4] # get locations 2, 3, and 4 from user's dashboard
            for location in locations: #for each get temps and add to location array to be sent to frontend
                city_weather = fetch_weather(location['name'])
                if city_weather:
                    main_temp = city_weather.get('main', {}).get('temp')
                    location['temperature'] = round(main_temp)
                else:
                    print("Failed to fetch weather data")
                    return jsonify({"error": "Failed to fetch weather data"}), 500
        else:
            locations = None
        weather_app_db.close()
    else:
        locations = None
        
    return render_template('index.html', db_connection_failed=db_connection_failed, userLoggedin=userLoggedin, userName=userName, locations=locations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    userLoggedin = session.get('userLoggedin', False)  # Ensure userLoggedin is defined
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Process the username and password (e.g., authenticate the user)
        print(f"Username: {username}, Password: {password}")
        weather_app_db.connect() #connect to DB
        user_id = weather_app_db.get_userid(username) #get user id from DB based on user given username
       
        if user_id: #If user is found in DB
            print(f"User ID: {user_id}")
            user_info = weather_app_db.get_user_info(user_id)
            session['userName'] = user_info['name'] #update session user name
            if user_info: #If user info is found in DB
                print(f"User Info: {user_info}")
                if password == user_info['password']: #if user given password matches the password in DB
                    print("User authenticated")
                    session['userLoggedin'] = True
                else:
                    error_message = "Invalid password."
                    session['userLoggedin'] = False
            else:
                error_message = "User information not found."
                session['userLoggedin'] = False
        else: 
            error_message = "Invalid username."
            session['userLoggedin'] = False
        
        weather_app_db.close() #close connection to DB

        if session['userLoggedin']:
            #update current location to most recent saved location
            weather_app_db.connect()
            saved_locations = weather_app_db.get_dashboardLocations(user_id)
            if saved_locations:
                city = saved_locations[0]['name']
            else:
                city = None
            weather_app_db.close()

            #redirect to index page with an alert and location if found
            if city:
                return redirect(url_for('index', alert_msg="You've been logged in successfully!", location=city))
            else:
                return redirect(url_for('index', alert_msg="You've been logged in successfully!")) 
       
        return render_template('login.html', return_message=error_message) #go back to login page with an error message
    return render_template('login.html') # this is return statement if login.request.method is not POST

@app.route('/logout')
def logout():
    session.pop('userLoggedin', None)
    session.pop('userName', None)
    return redirect(url_for('index', alert_msg="You've been successfully logged out!"))

@app.route('/dashboards')
def dashboards():
    userLoggedin = session.get('userLoggedin', False)
    userName = session.get('userName', None)
    locations = None

    if userLoggedin:
        try:
            weather_app_db.connect()
            user_id = weather_app_db.get_userid(userName)  # Retrieve user ID
            locations = weather_app_db.get_dashboardLocations(user_id)

            if locations:
                locations = locations[:5]  # Fetch up to 5 saved locations
                for location in locations:
                    city_weather = fetch_weather(location['name'])
                    tz_offset = 0
                    if city_weather:
                        main_temp = round(city_weather.get('main', {}).get('temp'))
                        weather_icon = city_weather.get('weather', [{}])[0].get('icon', '01d')
                        tz_offset = city_weather.get('timezone', 0)
                    else:
                        main_temp = "N/A"
                        weather_icon = '01d'  # Default icon if weather data is unavailable


                    pst_offset = timedelta(hours=-8)  # PST is UTC-8
                    current_date = (datetime.now(timezone.utc) + pst_offset).strftime("%m/%d/%Y")

                    offset = timedelta(seconds=tz_offset)

                    # Apply the offset to the UTC time and convert to PST
                    local_time = datetime.now(timezone.utc) + offset
                    local_time_pst = local_time.astimezone(timezone(timedelta(hours=0)))
                    current_time = local_time_pst.strftime("%-I:%M %p")

                    # Add weather data and time/date to the location dictionary
                    location['temperature'] = main_temp
                    location['weather_icon'] = weather_icon
                    location['time'] = current_time
                    location['date'] = current_date

                print("Fetched locations for dashboard:", locations)
            else:
                locations = []

            print(locations)
        except Exception as e:
            print("Error fetching locations:", e)
        finally:
            weather_app_db.close()

    return render_template('dashboard.html', userLoggedin=userLoggedin, locations=locations)

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Call the reusable fetch_weather function
    weather_data = fetch_weather(city)

    if not weather_data:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    return jsonify(weather_data)

@app.route('/add_location', methods=["POST","GET"])
def add_location():
    print("ADD LOCATION")
    weather_app_db.connect()  # Connect to the database
    try:
        city_name = request.args.get('city')
        print(city_name)
        if not city_name:
            return jsonify(error="City name is required"), 400

        user_id = weather_app_db.get_userid(session['userName'])  # Assuming session contains 'userName'
        if not user_id:
            return jsonify(error="User not found"), 404

        loc_id = weather_app_db.add_location(city_name)  # Add city to locations table if not exists
        weather_app_db.add_dashboardLocation(user_id, loc_id)  # Link the location to the user's dashboard
        print("Added!!!!!!!")
        return redirect(url_for('dashboards'))
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        weather_app_db.close()  # Ensure the connection is closed

@app.route('/remove_location', methods=["POST","GET"])
def remove_location():
    weather_app_db.connect()
    try:
        city_name = request.args.get('city')
        if not city_name:
            return jsonify(error="City name is required"), 400

        user_id = weather_app_db.get_userid(session['userName'])
        if not user_id:
            return jsonify(error="User not found"), 404

        loc_id = weather_app_db.get_locationID(city_name)  # Fetch the location ID for the given city
        if not loc_id:
            return jsonify(error="Location not found"), 404

        weather_app_db.delete_dashboardLocation(user_id, loc_id)  # Remove the location from user's dashboard
        return redirect(url_for('dashboards'))
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        weather_app_db.close()

@app.route('/load_saved_locations', methods=['GET'])
def load_saved_locations():
    weather_app_db.connect()
    try:
        user_id = weather_app_db.get_user_id(session['userName'])
        if not user_id:
            return jsonify(error="User not found"), 404

        locations = weather_app_db.get_dashboardLocations(user_id)  # Get all locations for the user's dashboard
        return jsonify(locations), 200  # Return as JSON
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        weather_app_db.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("AKSJHFDLKAJDHFLKSJHF")
    if request.method == 'POST':
        # Retrieve data from the request form
        username = request.form['username']
        password = request.form['password']

        print(f"Username: {username}, Password: {password}")
        # Check if the username already exists
        weather_app_db.connect()  # Connect to the database

        existing_user_id = weather_app_db.get_userid(username)

        if existing_user_id:  # If the username is already taken
            weather_app_db.close()  # Close the database connection
            error_message = "Username already exists. Please choose a different one."
            session['userLoggedin'] = False
            return redirect(url_for('register', alert_msg=error_message))
        
        new_user_id = weather_app_db.add_user({
            'name': username,
            'email': 'default@example.com', # keeping email in the database is tentative as we dont need it 
            'theme': 1,
            'temperatureUnit': 'C',
            'password': password
        })

        if new_user_id:  # If the user was successfully registered
            weather_app_db.close()  # Close the database connection
            success_message = "Registration successful! Please log in." # Registering user doesn't log them in right away
            return redirect(url_for('login', alert_msg=success_message))  # Redirect to the login page with a success message
        
        # If there was an error during registration
        weather_app_db.close()  # Close the database connection
        error_message = "Registration failed. Please try again later."
        return redirect(url_for('register', alert_msg=error_message))

    # Render the registration form for GET requests
    return render_template('register.html')

if __name__ == "__main__":
    port = 5000  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Port Number not specified. Using default port 5000.")
    app.run(debug=True, port=port)