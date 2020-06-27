#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for triggering a long running process
"""

import os
import logging as flog  # Flask app logs
from flask import Flask, jsonify, Response
from flask_cors import CORS  # To allow Swagger and other things to work
import json  # For parsing and creating json

# My modules
from .greeting_blueprint import greeting_blueprint

here = os.path.dirname(__file__)

flog.basicConfig(level=flog.DEBUG)

app = Flask(__name__, static_url_path='')

# we have some cross domain stuff behind nginx
CORS(app)

# Add blueprint views 
app.register_blueprint(greeting_blueprint, url_prefix='/pages')  # expose route: /greeting
app.debug = True

# Log the rules registered on the application, showing the blueprints
flog.info(f"app.url_map:{app.url_map}")


# ---------------------------------------------
# stations Utility functions
# ---------------------------------------------
def load_stations():
    """Read stations from storage"""
    return [
        {
            "ManufacturingSite": "San Dimas, CA",
            "JobType": "Being Excellent",
            "StationID": "666",
            "NetToSerialMac": "FE:ED:FA:CE:F0:0D"
        }
    ]


@app.route('/')
def index():
    return "Hello World!!"


# ------------------------
# stations routes
# ------------------------
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

# TODO:
# @app.route('/stations/<station_id>'  , methods=['PUT'])
# @app.route('/stations/<station_id>'  , methods=['DELETE'])
# ------------------------
