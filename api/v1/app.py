#!/usr/bin/python3
""" api/v1/app.py"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close the session after each call"""
    storage.close()

@app.errorhandler(404)
"""Designers are really creative when they have to design a “404 page” """
def not_found(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
