# this is the server
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from dotenv import load_dotenv
from weather_app_db import app_DB

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# OpenWeather API key (To be added)
API_KEY = os.getenv("OPENWEATHER_API_KEY")
weather_app_db = app_DB()

@app.route("/")
def home():
    print("SERVER IS RUNNING")
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400
# Fetch weather data from OpenWeather API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    weather_data = response.json()
    return jsonify(weather_data)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Process the username and password (e.g., authenticate the user)
        print(f"Username: {username}, Password: {password}")
        app_DB.get_userid(username, password)
        return redirect(url_for('index'))
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)