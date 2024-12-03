# this is the backend server 
# use "pip install flask" to install flask, which is the python framework to run a server 
# to run, type in python app.py in the terminal (dont forget to be in the project directory) 

# imports
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__) # use flask framework
CORS(app) #enables communication between frontend and backend

# Configure MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/weather_app' # db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Initialize extensions (SQLAlchemy)

# Location Model - Represents a saved location in the database
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the location
    city = db.Column(db.String(100), nullable=False)  # City name, must be provided

# Create tables in the database
with app.app_context():
    db.create_all()

#User Model : This is essentially a table that holds the user credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Route to fetch all saved locations from the database
@app.route('/dashboard/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()  # Query all locations from the database
    # Return locations as a JSON response
    return jsonify([{"id": loc.id, "city": loc.city} for loc in locations])

# Route to add a new location to the database
@app.route('/dashboard/locations', methods=['POST'])
def add_location():
    data = request.json  # Get the JSON data from the request
    city = data.get('city')  # Extract the city name from the data
    if city:
        new_location = Location(city=city)  # Create a new Location object
        db.session.add(new_location)  # Add new location to the database session
        db.session.commit()  # Commit the session to save changes to the database
        return jsonify({"message": "Location added"}), 201  # Return success message
    return jsonify({"error": "City name is required"}), 400  # Return error if city is not provided


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
    db.session.add(new_user) #INSERT INTO user (username, password) VALUES ('username', 'hashedpassword');
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# User login 
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the username exists
    user = User.query.filter_by(username=username).first() # SELECT * FROM user WHERE username = 'username' LIMIT 1;
    if user and bcrypt.check_password_hash(user.password, password):
        session["user_id"] = user.id  # Use Flask's session for stateful login
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401






#THESE ARE TESTS
# @app.route('/', methods=['GET'])
# def home():
#     return "Flask server is running. Use POST requests to interact with /login or /register routes.", 200


# @app.route('/login', methods=['POST'])
# def login():
#     # Mock response for login
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Simulate successful login
#     if username == "testuser" and password == "password123":
#         return jsonify({"message": "Login successful!"}), 200
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401

# @app.route('/register', methods=['POST'])
# def register():
#     # Mock response for registration
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Simulate successful registration
#     if username and password:
#         return jsonify({"message": f"User {username} registered successfully!"}), 201
#     else:
#         return jsonify({"error": "Missing username or password"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)