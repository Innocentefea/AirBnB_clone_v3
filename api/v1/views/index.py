#!/usr/bin/python3
"""
import app_views
create status route
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Create an endpoint that retrieves the number of each objects by type"""
    stats = {}
    stats['amenities'] = storage.count('Amenity')
    stats['cities'] = storage.count('City')
    stats['places'] = storage.count('Place')
    stats['reviews'] = storage.count('Review')
    stats['states'] = storage.count('State')
    stats['users'] = storage.count('User')
    return jsonify(stats)


@app_views.route('/status', methods=['GET'])
def get_status():
    """return a json status ok"""
    return jsonify({"status": "OK"})
