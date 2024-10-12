#!/usr/bin/python3
"""
Hello HBNB
This script initializes a Flask web application that responds with a greeting.
"""
from flask import Flask

app = Flask(__name__)  # Create an instance of the Flask class


@app.route('/', strict_slashes=False)
def home():
    """
    Home route that returns a greeting message.
    """
    return 'Hello HBNB!'  # Return the greeting message


if __name__ == "__main__":
    # Run the Flask application on the specified host and port
    app.run(host='0.0.0.0', port=5000)
