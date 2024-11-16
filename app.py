# this is the server
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project) 
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# OpenWeather API key (To be added)
API_KEY = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

if __name__ == "__main__":
    app.run(debug=True)