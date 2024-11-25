# this is the backend server 
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 

# imports
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__) # use flask framework

# Configure MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/weather_app' # db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#User Model : This is essentially a table that holds the user credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create tables in the database
with app.app_context():
    db.create_all()
