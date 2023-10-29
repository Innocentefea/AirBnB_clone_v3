#!/usr/bin/python3
"""
import app_views
create status route
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """return a json status ok"""
    return jsonify({"status": "OK"})
