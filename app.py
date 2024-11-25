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

# User Registeration
@app.route("/register", methods=["POST"])
def register():
    data = request.json # This is the json file that holds the username and password from the post request
    username = data.get("username")
    password = data.get("password")

    #Check if no username/password entered
    if not username or not password: 
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password and save the user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201
