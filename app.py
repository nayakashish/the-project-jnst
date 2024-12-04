# this is the server
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from dotenv import load_dotenv
from weather_app_db import app_DB

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
            locations = locations[:3] #get first 3 locations from user's dashboard
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
            return redirect(url_for('index', alert_msg="You've been logged in successfully!")) #redirect to index page with an alert
        return render_template('login.html', return_message=error_message) #go back to login page with an error message
    return render_template('login.html') # this is return statement if login.request.method is not POST

@app.route('/logout')
def logout():
    session.pop('userLoggedin', None)
    session.pop('userName', None)
    return redirect(url_for('index', alert_msg="You've been successfully logged out!"))

@app.route('/dashboards')
def dashboards():
    #TODO - check if user is logged in
    return render_template('dashboard.html')

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

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/add_location', methods=['POST'])
def add_location():
    city = request.json.get('city')
    if city and city not in locations:
        locations.append(city)
        return jsonify(message="Location added successfully"), 200
    return jsonify(error="Location already exists or invalid"), 400