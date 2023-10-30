#!/usr/bin/python3
"""Create a new view for Place objects that handles
all default RESTFul API actions:"""

from flask import jsonify, request, abort
from models.state import State
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City: GET"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object. : GET"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object: DELETE"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place: POST"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object: PUT"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for Place objects based on the JSON request body"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if not states and not cities:
        places = storage.all(Place).values()
    else:
        # Retrieve places based on states
        for state_id in states:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    if city not in cities:
                        cities.append(city)

        # Retrieve places based on cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city is not None:
                places.extend(city.places)

    if amenities:
        amenities_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
        places = [place for place in places if all(amenity in place.amenities for amenity in amenities_objs)]

    return jsonify([place.to_dict() for place in places])
