# this is the server
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 
import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# OpenWeather API key (To be added)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/")
def home():
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

if __name__ == "__main__":
    app.run(debug=True)