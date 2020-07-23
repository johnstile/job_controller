""" API V1
REF: https://realpython.com/flask-blueprint/
REF: https://www.flaskapi.org/api-guide/status-codes/
"""

from flask import Blueprint, current_app, jsonify, request, abort
import json  # For parsing and creating json
import uuid  # For unique ids of stations
from flask_redis import FlaskRedis  # For persistent storage of stations
import redis  # for exception handling
from flask_api import status  # To return named http status codes
from werkzeug.local import LocalProxy  # Allow logging to app.logger
from werkzeug.exceptions import HTTPException

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt_claims
)

# Allow logging to app.logger
logger = LocalProxy(lambda: current_app.logger)

# object name                 (<decor_name>    , <import_name>)
api_v1_blueprint = Blueprint('api_v1_blueprint', __name__)

jwt = JWTManager()


@api_v1_blueprint.route('/version')
def index():
    return {"API Version": "v1"}, status.HTTP_200_OK


# ---------------------------------------------
# STATIONS UTILITY FUNC: BEGIN
# ---------------------------------------------
def load_stations():
    """Read stations from storage
    :return: list of dict
    """
    logger.debug(f"Called load_stations")
    try:
        # Persistent storage for stations
        redis_conn = FlaskRedis(current_app)
        loaded_stations = redis_conn.get('stations')
        logger.debug(f"loaded_stations: {loaded_stations}")
    except redis.exceptions.ConnectionError:
        raise RedisConnectionError(
            'DataService not accessible',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    if loaded_stations:
        return json.loads(loaded_stations)
    else:
        return []


def save_stations(stations):
    """Write stations to storage
    :param stations: Json Dict of all stations
    """
    logger.debug(f"Called save_stations: {stations}")
    try:
        redis_conn = FlaskRedis(current_app)
        redis_conn.set('stations', json.dumps(stations))
    except redis.exceptions.ConnectionError:
        raise RedisConnectionError(
            'DataService not accessible',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return {"status": "success"}


def change_station(station_id, request_data):
    """Change station from stations
    :param station_id: user defined stationId
    :param request_data: change set object
    :return: string
    """
    if not request_data:
        abort(status.HTTP_400_BAD_REQUEST)

    logger.debug(f"Call change_station: {station_id}, {request_data}")
    # Prepare change set
    new_data = json.loads(request_data)
    # Load old data into structure
    stations = load_stations()

    try:
        # Check if the StationID is used by different station
        if station_id != new_data['StationID']:
            duplicate_index = find_index_in_list_of_dict(
                lst=stations,
                key='StationID',
                value=new_data['StationID']
            )
            if duplicate_index:
                raise StationsDuplicateError(
                    'StationId Not Available',
                    status_code=status.HTTP_409_CONFLICT
                )
    except StationsRequestError:
        logger.debug(f"New StationId Available")

    # Find index of old StationId
    target_index = find_index_in_list_of_dict(
        lst=stations,
        key='StationID',
        value=station_id
    )
    stations[target_index] = new_data

    # save changes
    save_stations(stations)
    logger.info(f"Updated stations index: {target_index}")
    return {"status": "success"}


def delete_station(station_id):
    """Delete station from stations
    :param station_id:
    :return: string
    """
    logger.debug(f"Call delete_stations: {station_id}")
    # Load old data into structure
    stations = load_stations()
    # Find index in list of stations
    target_index = find_index_in_list_of_dict(
        lst=stations,
        key='StationID',
        value=station_id
    )
    # remove from list by index
    stations.remove(stations[target_index])
    # save changes
    save_stations(stations)

    return {"status": "success"}


def add_station(request_data):
    """Add to stations.json structure
    :param request_data: Json payload data from browser
    """
    if not request_data:
        abort(status.HTTP_400_BAD_REQUEST)

    # Load old data into structure
    stations = load_stations()
    if 'error' in stations:
        logger.info(f"Load Stations Had Error:{stations}")

    # Load http post data into structure
    new_data = json.loads(request_data)

    # Sanitize user input
    # Could ensure values are barcode friendly
    # data.update((k, make_code39(v)) for k, v in data.items())
    # Check if the new StationId is already in use

    try:
        duplicate_index = find_index_in_list_of_dict(
            lst=stations,
            key='StationID',
            value=new_data['StationID']
        )
        if duplicate_index:
            raise StationsDuplicateError(
                'StationId Not Available',
                status_code=status.HTTP_409_CONFLICT
            )
    except StationsRequestError:
        logger.debug(f"New StationId Available")

    logger.info(f"New Station:{new_data}")
    stations.append(new_data)
    for station in stations:
        if 'id' not in station:
            # Add a unique identifier
            station['id'] = str(uuid.uuid4())

    logger.info(f"stations:{stations}")
    return save_stations(stations)


def find_index_in_list_of_dict(lst, key, value):
    """Search list of dictionaries for index where key == value
    :param lst: List of Dict to be searched
    :param key: Dict Key
    :param value: Value of Dict Key
    :return: int Index
    """
    logger.debug(f"Call find_index_in_list_of_dict: {lst}, {value}")
    fount_index = -1  # default
    for this_index, lst in enumerate(lst):
        if lst[key] == value:
            fount_index = this_index
            break
    logger.debug(f"found_index: {fount_index}")
    if fount_index == -1:
        raise StationsRequestError(
            'StationId Not Found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return fount_index


# ---------------------------------------------
# STATIONS UTILITY FUNC: END
# ---------------------------------------------
# ---------------------------------------------
# AUTHENTICATION UTILITY FUNC: BEGIN
# ---------------------------------------------


def authenticate_user(username, password):
    """Determine if this is a valid user
    :param username: string
    :param password: string
    :return: backendError | authError | Authorized
    """
    # TODO: Choose storage solution backend
    logger.debug(
        f"username:{username}, password:{password}"
    )
    responses = ["backendError", "authError", "Authorized"]
    return responses[2]


class UserObject:
    """Data stuffed in JWT Bearer"""
    def __init__(self, username, roles):
        self.username = username
        self.roles = roles

    def serialize(self):
        """
        Python3 classes can't be serialized
        This operates correctly
        REF: https://stackoverflow.com/questions/21411497/flask-jsonify-a-list-of-objects 
        """
        return {
            'username': self.username,
            'roles': self.roles 
        }


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    """Called when create_access_token is used
    Returns custom claims added to token
    """
    logger.debug(f"Called user_claims_loader: {user}")
    return {'roles': user.roles}


@jwt.user_identity_loader
def user_identity_lookup(user):
    """Called when create_access_token is used.
    Returns identity in the token
    of the access token should be.
    """
    logger.debug(f"Called user_identity_lookup. username:{user.username}")
    return user.username


# ---------------------------------------------
# AUTHENTICATION UTILITY FUNC: END
# ---------------------------------------------
# --------------------------------------------
# STATIONS API: BEGIN
# --------------------------------------------

@api_v1_blueprint.route('/stations', methods=['GET'])
def stations_get():
    """Get stations
    :return: Json List of Dict
    """
    logger.debug("Called stations_get")
    return jsonify(load_stations()), status.HTTP_200_OK


@api_v1_blueprint.route('/stations', methods=['POST'])
def stations_add():
    """Create new station, Return id of added station.
    :return: Json Dict with id
    """
    logger.debug(f"Called stations_add: {request.data}")
    result = add_station(request.data)
    return result, status.HTTP_201_CREATED


@api_v1_blueprint.route('/stations/<station_id>', methods=['PUT'])
def stations_update(station_id):
    """Change station identified by id param with payload data
    :param station_id: String
    :return: Json Dict with id
    """
    logger.debug(f"Called stations_update: {station_id}")

    if not request.data:
        abort(status.HTTP_409_CONFLICT)

    result = change_station(station_id, request.data)
    return result, status.HTTP_202_ACCEPTED


@api_v1_blueprint.route('/stations/<station_id>', methods=['DELETE'])
def stations_delete(station_id):
    """
    Remove station identified by id param
    :param station_id: String
    :return: Json Dict with id
    """
    logger.debug(f"Called stations_delete: {station_id}")
    result = delete_station(station_id)
    return result, status.HTTP_202_ACCEPTED


# --------------------------------------------
# STATIONS API: END
# --------------------------------------------
# --------------------------------------------
# AUTHENTICATION API: BEGIN
# --------------------------------------------


@api_v1_blueprint.route('/login', methods=['POST'])
def login():
    """Login will create a token"""
    logger.debug(f"Calling Login: {request.json}")

    if not request.is_json:
        abort(status.HTTP_401_UNAUTHORIZED, description="Missing all")

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        abort(status.HTTP_401_UNAUTHORIZED, description="Missing username")
    if not password:
        abort(status.HTTP_401_UNAUTHORIZED, description="Missing password")

    result = authenticate_user(username, password)
    logger.debug(f"result:{result}")

    # backend service failure
    if 'backendError' in result:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, description="Failed lookup")

    # Failed auth
    if 'authError' in result:
        abort(status.HTTP_403_FORBIDDEN, description="Bad username or password")

    # Generate Token
    user = UserObject(username=username, roles=['admin', 'user'])
    # Python3:  jwt.encode fails with “Object of type 'bytes' is not JSON serializable”
    # This method returns a dict of the class, which works
    access_token = create_access_token(identity=user.serialize())
    ret = {'access_token': access_token}

    return ret, status.HTTP_202_ACCEPTED


@api_v1_blueprint.route('/auth_check', methods=['GET'])
@jwt_required
def protected():
    """Use to check if the browsers token is valid"""
    # Access the identity of the current user with get_jwt_identity
    logger.info(f"Called protected: headers: {request.headers}")
    user = get_jwt_identity()
    claims = get_jwt_claims()
    return {"user": user, "claims": claims}, status.HTTP_202_ACCEPTED


# --------------------------------------------
# AUTHENTICATION API: END
# --------------------------------------------
# --------------------------------------------
# Exceptions:
#  API best practices: servers don't return error stack-trace
#  exceptions should be handled, and
#  exception handler makes consistent structured response
#  - Identify what could go wrong
#  - Return useful information to the client
#  - Don't leak too much information
# --------------------------------------------
class ApiError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@api_v1_blueprint.errorhandler(ApiError)
def handle_invalid_usage(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class RedisConnectionError(ApiError):
    """Database Not Accessible"""


class StationsError(ApiError):
    """Base Station Error"""


class StationsRequestError(StationsError):
    """Threat Stack request error."""


class StationsDuplicateError(StationsError):
    """Threat Stack request error."""
