""" API V1
REF: https://realpython.com/flask-blueprint/
REF: https://www.flaskapi.org/api-guide/status-codes/
"""

from flask import Blueprint, current_app, jsonify, Response, request, abort
import json  # For parsing and creating json
import uuid  # For unique ids of stations
from flask_redis import FlaskRedis  # For persistent storage of stations
from flask_api import status  # To return named http status codes

# object name                 (<decor_name>       , <import_name>)
api_v1_blueprint = Blueprint('api_v1_blueprint', __name__)


# Add a View
@api_v1_blueprint.route('/version')
def index():
    return {"API Version": "v1"}, status.HTTP_200_OK


# ---------------------------------------------
# BEGIN: stations Utility functions
# ---------------------------------------------
def load_stations():
    """Read stations from storage
    :return: list of dict
    """
    current_app.logger.debug(f"Called load_stations")
    # Persistent storage for stations
    redis_conn = FlaskRedis(current_app)
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
    current_app.logger.debug(f"Called save_stations: {stations}")
    try:
        redis_conn = FlaskRedis(current_app)
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
    current_app.logger.debug(f"Call update_stations: {station_id}, {request_data}")
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
            raise current_app.StationsRequestError
        stations[target_index] = new_data
        # save changes
        save_stations(stations)
        current_app.logger.info(f"Updated stations index: {target_index}")
        return_value = 0

    except Exception as e:
        current_app.logger.debug(
            f"Error in update_stations() for id {station_id}. Error:{str(e)}"
        )
        return_value = -1

    return return_value


def delete_stations(station_id):
    """Delete station from stations
    :param station_id:
    :return: string
    """
    current_app.logger.debug(f"Call delete_stations: {station_id}")
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
            raise current_app.StationsRequestError
        # remove from list by index
        stations.remove(stations[target_index])
        # save changes
        save_stations(stations)
        return_value = 0

    except Exception as e:
        current_app.logger.error(
            f"Error in delete_stations for id {station_id}"
        )
        current_app.logger.error(f"Error:{str(e)}")
        return_value = -1

    return return_value


def add_stations(request_data):
    """Add to stations.json structure
    :param request_data: Json payload data from browser
    """
    # Load old data into structure
    stations = load_stations()
    if 'error' in stations:
        current_app.logger.info(f"Load Stations Had Error:{stations}")

    # Load http post data into structure
    data = json.loads(request_data)

    # Sanitize user input
    # Could ensure values are barcode friendly
    # data.update((k, make_code39(v)) for k, v in data.items())

    current_app.logger.info(f"New Station:{data}")
    stations.append(data)
    for station in stations:
        if 'id' not in station:
            # Add a unique identifier
            station['id'] = str(uuid.uuid4())

    current_app.logger.info("stations:{stations}")
    return save_stations(stations)


def find_index_in_list_of_dict(lst, key, value):
    """Search list of dictionaries for index where key == value
    :param lst: List of Dict to be searched
    :param key: Dict Key
    :param value: Value of Dict Key
    :return: int Index
    """
    current_app.logger.debug(f"Call find_index_in_list_of_dict: {lst}, {value}")
    fount_index = -1  # default
    for this_index, lst in enumerate(lst):
        if lst[key] == value:
            fount_index = this_index
            break
    current_app.logger.debug(f"found_index: {fount_index}")
    return fount_index


# ---------------------------------------------
# BEGIN: stations Utility functions
# ---------------------------------------------

# --------------------------------------------
# STATIONS API: BEGIN
# --------------------------------------------

@api_v1_blueprint.route('/stations', methods=['GET'])
def stations_get():
    """Get stations
    :return: Json List of Dict
    """
    current_app.logger.debug("Called stations_get")
    try:
        return jsonify(load_stations())

    except Exception as e:
        response = {'status': 'failure', 'error': str(e)}
        current_app.logger.error(f"error:{response}")
        http_code = 400

    return Response(
        json.dumps(
            response, sort_keys=True, indent=4, separators=(',', ': ')
        ),
        mimetype="application/json"
    ), http_code


@api_v1_blueprint.route('/stations', methods=['POST'])
def stations_add():
    """Crate a new station, Return id of added station.
    :return: Json Dict with id
    """
    current_app.logger.debug(f"Called stations_add: {request.data}")
    if not request.data:
        abort(status.HTTP_409_CONFLICT)
    try:
        result = add_stations(request.data)
        if "success" in result:
            return result, status.HTTP_201_CREATED
        else:
            raise current_app.StationsRequestError
    except Exception as e:
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@api_v1_blueprint.route('/stations/<station_id>', methods=['PUT'])
def stations_update(station_id):
    """Change station identified by id param with payload data
    :param station_id: String
    :return: Json Dict with id
    """
    current_app.logger.debug(f"Called stations_update: {station_id}")
    if not request.data:
        abort(status.HTTP_409_CONFLICT)
    result = update_stations(station_id, request.data)
    if result == -1:
        abort(status.HTTP_409_CONFLICT)
    else:
        return {'id': station_id}, status.HTTP_202_ACCEPTED


@api_v1_blueprint.route('/stations/<station_id>', methods=['DELETE'])
def stations_delete(station_id):
    """
    Remove station identified by id param
    :param station_id: String
    :return: Json Dict with id
    """
    current_app.logger.debug(f"Called stations_delete: {station_id}")
    result = delete_stations(station_id)
    if result != -1:
        return {'id': station_id}, status.HTTP_202_ACCEPTED
    else:
        abort(status.HTTP_409_CONFLICT)

# --------------------------------------------
# STATIONS API: END
# --------------------------------------------
