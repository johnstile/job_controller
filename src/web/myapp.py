#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for triggering a long running process
"""

import os
import logging as flog  # Flask app logs
from flask import Flask, jsonify, Response, request, abort
from flask_cors import CORS  # To allow Swagger and other things to work
import json  # For parsing and creating json
import uuid  # For unique ids of stations
from flask_redis import FlaskRedis  # For persistent storage of stations

# My modules
from .greeting_blueprint import greeting_blueprint


class StationsError(Exception):
    """Base Station Error"""
    status_code = 400


class StationsRequestError(StationsError):
    """Threat Stack request error."""


class StationsAPIError(StationsError):
    """Threat API Stack error."""


here = os.path.dirname(__file__)

flog.basicConfig(level=flog.DEBUG)

app = Flask(__name__, static_url_path='')

app.config.from_pyfile(os.path.join(here, 'flask.cfg'))

# Persistent storage for stations
redis_conn = FlaskRedis(app)

# we have some cross domain stuff behind nginx
CORS(app)

# Add blueprint views
# expose route: /greeting under /V1/greeting
app.register_blueprint(greeting_blueprint, url_prefix='/V1')

# Log the rules registered on the application, showing the blueprints
flog.info(f"app.url_map:{app.url_map}")


# ---------------------------------------------
# BEGIN: stations Utility functions
# ---------------------------------------------
def load_stations():
    """Read stations from storage
    :return: list of dict
    """
    flog.debug(f"Called load_stations")
    stations_file = os.path.join("stations.json")
    loaded_stations = redis_conn.get('stations')
    if loaded_stations:
        return json.loads(loaded_stations)
    else:
        # Maybe no stations defined
        return [
            {
                "ManufacturingSite": "San Dimas, CA",
                "JobType": "Being Excellent",
                "StationID": "666",
                "NetToSerialMac": "FE:ED:FA:CE:F0:0D"
            }
        ]


def save_stations(stations):
    """Write stations to storage
    :param stations: Json Dict of all stations
    """
    flog.debug(f"Called save_stations: {stations}")
    try:
        redis_conn.set('stations', json.dumps(stations))
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}


def update_stations(station_id, request_data):
    """Delete station from stations
    :param station_id: user defined stationId
    :param request_data: change set object
    :return: string
    """
    flog.debug(f"Call update_stations: {station_id}, {request_data}")
    try:
        # Prepare change set
        new_data = json.loads(request_data)
        # Load old data into structure
        stations = load_stations()
        # Find index in list of stations
        target_index = find_index_in_list_of_dict(
            lst=stations,
            key='StationID',
            value=station_id
        )
        if target_index == -1:
            raise StationsRequestError
        stations[target_index] = new_data
        # save changes
        save_stations(stations)
        flog.info(f"Updated stations index: {target_index}")
        return_value = 0

    except Exception as e:
        app.logger.debug(
            f"Error in update_stations() for id {station_id}. Error:{str(e)}"
        )
        return_value = -1

    return return_value


def delete_stations(station_id):
    """Delete station from stations
    :param station_id:
    :return: string
    """
    flog.debug(f"Call delete_stations: {station_id}")
    try:
        # Load old data into structure
        stations = load_stations()
        # Find index in list of stations
        target_index = find_index_in_list_of_dict(
            lst=stations,
            key='StationID',
            value=station_id
        )
        if target_index == -1:
            raise StationsRequestError
        # remove from list by index
        stations.remove(stations[target_index])
        # save changes
        save_stations(stations)
        return_value = 0

    except Exception as e:
        app.logger.error(
            f"Error in delete_stations for id {station_id}"
        )
        app.logger.error(f"Error:{str(e)}")
        return_value = -1

    return return_value


def add_stations(request_data):
    """Add to stations.json structure
    :param request_data: Json payload data from browser
    """
    # Load old data into structure
    stations = load_stations()
    if 'error' in stations:
        app.logger.info(f"Load Stations Had Error:{stations}")

    # Load http post data into structure
    data = json.loads(request_data)

    # Sanitize user input
    # Could ensure values are barcode friendly
    # data.update((k, make_code39(v)) for k, v in data.items())

    app.logger.info(f"New Station:{data}")
    stations.append(data)
    for station in stations:
        if 'id' not in station:
            # Add a unique identifier
            station['id'] = str(uuid.uuid4())

    app.logger.info("stations:{stations}")
    return save_stations(stations)


def find_index_in_list_of_dict(lst, key, value):
    """Search list of dictionaries for index where key == value
    :param lst: List of Dict to be searched
    :param key: Dict Key
    :param value: Value of Dict Key
    :return: int Index
    """
    flog.debug(f"Call find_index_in_list_of_dict: {lst}, {value}")
    fount_index = -1  # default
    for this_index, lst in enumerate(lst):
        if lst[key] == value:
            fount_index = this_index
            break
    flog.debug(f"found_index: {fount_index}")
    return fount_index

# ---------------------------------------------
# BEGIN: stations Utility functions
# ---------------------------------------------


@app.route('/')
def index():
    return "Hello Job Controller!!"


# --------------------------------------------
# STATIONS API: BEGIN
# --------------------------------------------

@app.route('/stations', methods=['GET'])
def stations_get():
    """Get stations
    :return: Json List of Dict
    """
    flog.debug("Called stations_get")
    try:
        return jsonify(load_stations())

    except Exception as e:
        response = {'status': 'failure', 'error': str(e)}
        flog.error(f"error:{response}")
        http_code = 400

    return Response(
        json.dumps(
            response, sort_keys=True, indent=4, separators=(',', ': ')
        ),
        mimetype="application/json"
    ), http_code


@app.route('/stations', methods=['POST'])
def stations_add():
    """Crate a new station, Return id of added station.
    :return: Json Dict with id
    """
    flog.debug(f"Called stations_add: {request.data}")
    if not request.data:
        abort(409)
    try:
        result = add_stations(request.data)
        return result
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json"), 500


@app.route('/stations/<station_id>', methods=['PUT'])
def stations_update(station_id):
    """Change station identified by id param with payload data
    :param station_id: String
    :return: Json Dict with id
    """
    flog.debug(f"Called stations_update: {station_id}")
    if not request.data:
        abort(409)
    result = update_stations(station_id, request.data)
    if result != -1:
        return Response(json.dumps({'id': station_id}), mimetype="application/json"), 200
    else:
        abort(409)


@app.route('/stations/<station_id>', methods=['DELETE'])
def stations_delete(station_id):
    """
    Remove station identified by id param
    :param station_id: String
    :return: Json Dict with id
    """
    flog.debug(f"Called stations_delete: {station_id}")
    result = delete_stations(station_id)
    if result != -1:
        return {'id': station_id}
        # return Response(
        #     json.dumps({'id': station_id}), mimetype="application/json"), 200
    else:
        abort(409)

# --------------------------------------------
# STATIONS API: END
# --------------------------------------------

@app.route('/echo_request')
def echo_request():
    """API independent route to ensure things are working"""
    return jsonify(dict(request.headers))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0')
