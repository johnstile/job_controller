""" API V1
REF: https://realpython.com/flask-blueprint/
REF: https://www.flaskapi.org/api-guide/status-codes/
"""

import os  # For accessing the logs dir
from flask import Blueprint, current_app, jsonify, request, abort
import json  # For parsing and creating json
import uuid  # For unique ids of stations
import time  # For job id
from flask_redis import FlaskRedis  # For persistent storage of stations
import redis  # for exception handling
from flask_api import status  # To return named http status codes
from werkzeug.local import LocalProxy  # Allow logging to app.logger
from werkzeug.exceptions import HTTPException

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt_claims
)

from rq import exceptions as RqExceptions
from rq import cancel_job
from redis import Redis
from util.redis_killer import KillQueue, KillWorker, KillJob
from util.job_methods import sleep_and_count
from rq import cancel_job

# Allow logging to app.logger
logger = LocalProxy(lambda: current_app.logger)

# object name                 (<decor_name>    , <import_name>)
api_v1_blueprint = Blueprint('api_v1_blueprint', __name__)

jwt = JWTManager()

# TODO: Choose storage solution backend
job_logs_dir = os.path.join('/app/job_logs')

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
# ---------------------------------------------
# JOBS UTILITY FUNC: BEGIN
# ---------------------------------------------
def get_jobs_list(current_job, show_n_jobs, step):
    """Return all jobs, active or not
    Using the job timestamp as the job_id (YYYYMMDD_HHMMSS)
    :param show_n_jobs: size of list of jobs to show
    :param current_job: date of folder for first element in group
    :param step: pages to step in a direction (+/-)
    :return:  list of dict
    """
    logger.info(
        (
            "Called get_job_list() with "
            "show_n_builds:{}, "
            "current_id:{}, "
            "step:{}"
        ).format(
            show_n_jobs,
            current_job,
            step
        )
    )
    # Full list of job logs
    jobs_list = sorted(os.listdir(job_logs_dir), reverse=True)
    logger.info("==>jobs_list: {}".format(jobs_list))

    jobs_list_length = len(jobs_list)
    logger.info("==>jobs_list_length: {}".format(jobs_list_length))

    # Get the index of the current job, or use 0
    # But they may have removed the current job
    if current_job:
        try:
            current_index = jobs_list.index(current_job)
        except ValueError:
            current_index = 0
    else:
        current_index = 0
    logger.info("==>current_index: {}".format(current_index))

    if step:
        step = int(step)
    else:
        step = 0
    logger.info("==>step: {}".format(step))

    # From option "show_n_jobs" figure out size limit
    limit = len(jobs_list)
    if show_n_jobs:
        limit = int(show_n_jobs)
    logger.info("==>limit: {}".format(limit))

    new_start_index = current_index + limit * step
    logger.info("==>new_start_index:{}".format(new_start_index))

    # Protection from list bounds
    if new_start_index < 0:
        new_start_index = 0
    elif new_start_index >= jobs_list_length - limit:
        new_start_index = jobs_list_length - limit
    logger.info("==>new_start_index:{}".format(new_start_index))

    # default to size of length (shows small number of jobs)
    new_end_index = new_start_index + limit
    # default to jobs_list_length (shows all jobs)
    # new_end_index = jobs_list_length
    logger.info("==>new_end_index:{}".format(new_end_index))

    job_dir_sublist = jobs_list[new_start_index:new_end_index]
    logger.info("==>job_dir_sublist:{}".format(job_dir_sublist))

    # Look inside each dir for params and status
    job_configs = []
    for job_dir in job_dir_sublist:
        job_config_file = os.path.join(job_logs_dir, job_dir, "job_scheduled.json")
        with open(job_config_file, 'r') as fh_config:
            job_config = json.load(fh_config)
            logger.info("log:{}, config:{}".format(job_dir, job_config))
            job_configs.append(
                {
                    "jobType": job_config['Fixture']['JobType'],
                    'workOrder': str(job_config['Input']['WorkOrder']),
                    'stationId': job_config['Fixture']['StationID'],
                    'manufacturingSite': job_config['Fixture']['ManufacturingSite'],
                    'operatorId': job_config['Input']['Operator'],
                    'partNumber': job_config['Input']['PartNumber'],
                    'serialNumber': job_config['Input']['SerialNumber'],
                    'Date': job_dir,
                    'Status': job_config['Status']
                }
            )

    # Ask Redis for status of jobs in our list
    redis_jobs = get_job_queue()
    for redis_job in redis_jobs:
        logger.info("==>redis_job: {}".format(redis_job))
        job_config = next((job_config for job_config in job_configs if job_config['Date'] == redis_job['job_id']), None)
        if job_config:
            job_config['Status'] = redis_job['status']

    return {"total_jobs": len(jobs_list), "configs": job_configs}

def get_job_queue():
    """
    Return jobs running or scheduled
    - Scheduled jobs are in the Queue
    - Running jobs are in Workers
    :return: a list of dict, with job_id, status, and form fields from the Run Test page
    """
    jobs = []  # will return this list
    redis_conn = FlaskRedis(current_app)
    q = KillQueue('JOB', connection=redis_conn)
    logger.info('q:{}'.format(q))
    logger.info('get_jobs:{}'.format(q.get_jobs))
    # Get scheduled jobs from Queue
    for job in q.jobs:
        logger.info('\tScheduled Job:{}'.format(job))
        job_config = parse_config(job.id)
        job_config['job_id'] = job.id
        job_config['status'] = "scheduled"
        jobs.append(job_config)

    # Get running jobs from Workers
    workers = KillWorker.all(queue=q)
    logger.info('workers:{}'.format(workers))
    for worker in workers:
        job = worker.get_current_job()
        if job:
            job_config = parse_config(job.id)
            job_config['job_id'] = job.id
            job_config['status'] = "running"
            job_config['pid'] = worker.pid
            jobs.append(job_config)

    logger.info('Total Found jobs:{}'.format(jobs))
    return jobs

def parse_config(job_id):
    """Read the config file from the job log
    :return:  dict with job parameters
    """
    logger.debug("Get config")
    log_dir_run = os.path.join(job_logs_dir, job_id)
    config_run_file = os.path.join(log_dir_run, "job_scheduled.json")
    logger.debug("config_run_file: {}".format(config_run_file))

    with open(config_run_file, 'r') as config_fh:
        config_data = json.load(config_fh)
        return config_data

# ---------------------------------------------
# JOBS UTILITY FUNC: BEGIN
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
# JOB API: BEGIN
# --------------------------------------------
# Ideas for routes.
# jobs_list()      GET  /jobs
# job_post()       POST /jobs
# job_change()     PUT  /jobs/{id}
# --------------------------------------------
@api_v1_blueprint.route('/jobs', methods=['GET'])
def job_list():
    """Get all jobs and important params
    current_job: log folder name
    steps: int: number of steps  (e.g. +/- 5
    show_n_jobs int: number of jobs to show (default: all)
    Return: list of dict as json, with params and job status
    """
    current_job = request.args.get('current_job') or None
    show_n_jobs = request.args.get('show_n_jobs')
    step = request.args.get('step') or 0

    logger.info(
        (
            'Called job_list() route:GET /jobs?current_job={}&show_n_jobs={}&step=step'
        ).format(
            current_job,
            show_n_jobs,
            step
        )
    )
    jobs = get_jobs_list(current_job=current_job, show_n_jobs=show_n_jobs, step=step)
    if jobs is None:
        return {'error': "No Jobs found"}, status.HTTP_400_BAD_REQUEST
    else:
        return json.dumps(jobs, sort_keys=True, indent=4, separators=(',', ': ')), status.HTTP_200_OK



@api_v1_blueprint.route("/jobs", methods=['POST'])
def job_new():
    """Start a job
    receive a json with info from the user.
    """
    logger.info('Called job_new()');

    if not request.json:
        abort(400)

    # this is used as the log directory name & Redis pubsub stream
    now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    logger.info('now: {}'.format(now))

    # Store posted request
    job_request = request.get_json()
    logger.info('Job Request: {}'.format(job_request))

    # Load stations
    stations = load_stations()
    if 'error' in stations:
        logger.error("Load Stations Had Error:{}".format(stations))
        return {"error": "Station Unavailable", "jobId": now}, status.HTTP_503_SERVICE_UNAVAILABLE

    # Locate the station based on job request
    station = next(
        (x for x in stations if x['StationID'] == job_request['StationID']),
        None
    )

    if station is not None:
        logger.info("Found Station:{}".format(station))
    else:
        logger.critical("Not Found Station:{}".format(station))
        return {"error": "Station Not Found", "jobId": now}, status.HTTP_404_NOT_FOUND

    # Create job config file, consumed by test 
    job_config = {}

    job_config['Input'] = {
        'SerialNumber': job_request['SerialNumber'],
        'WorkOrder': job_request['WorkOrder'],
        'Operator': job_request['Operator'],
        'StationID' : job_request['StationID']
    }

    job_config['Fixture'] = {
        'StationID': station['StationID'],
        'JobType': station['JobType'],
        'ManufacturingSite': station['ManufacturingSite']
    }

    job_config['Comm'] = {
        "Type": "network",
        "Port": 50000,
        "NetToSerialMac": station['NetToSerialMac'],
        "NetAddr": None,
        "TimeOut": 30,
        "Debug": True
    }

    job_config['Log'] = {'Level': 'debug'}

    job_config['Data'] = now
    job_config['Status'] = 'scheduled'
    #
    # Make dir for all jobs
    #
    if not os.path.isdir(job_logs_dir):
        os.mkdir(job_logs_dir)
    #
    # Make dir for this job
    #
    job_log_dir = os.path.join(job_logs_dir, now)
    if not os.path.isdir(job_log_dir):
        os.mkdir(job_log_dir)
    #
    # Write this job config file
    # 'now' is used for both job id and directory name, to find the config
    #
    job_config_file = os.path.join(job_logs_dir, now, "job_scheduled.json")
    with open(job_config_file, 'w') as fh_config:
        json.dump(job_config, fh_config, sort_keys=True, indent=4, separators=(',', ': '))
    logger.info("Saved :{}".format(job_config_file))
    #
    # Add job to the 'JOB' queue
    #
    redis_conn = FlaskRedis(current_app)
    q = KillQueue('JOB', connection=redis_conn)  # no args implies the default queue
    q_before = len(q)
    job = q.enqueue(
        sleep_and_count,
        job_configuration_file=job_config_file,
        now=now,
        job_id=now,
        job_timeout=2600
    )
    # Collect some info about the job
    try:
        job_id = job.id
        logger.info("The job is queued: {}".format(job_id))
        msg = {"msg": "Enqueued", "jobId": job_id}
        response = jsonify(msg), status.HTTP_201_CREATED
    except RqExceptions.NoSuchJobError as e:
        msg = {"error": str(e), "jobId": now}
        response = jsonify(msg), status.HTTP_404_NOT_FOUND
    except AttributeError as e:
        msg = {"error": str(e), "jobId": now}
        response = jsonify(msg), status.HTTP_418_IM_A_TEAPOT
    logger.info('Job id: {}, msg:{}'.format(now, msg))
    return response

# --------------------------------------------
# JOB API: END
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
