# use "pip install flask" to install flask, which is the python framework to run a server 
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to My Flask Web Server!</h1>"

if __name__ == "__main__":
    app.run(debug=True)