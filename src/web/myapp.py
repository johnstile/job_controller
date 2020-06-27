#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for triggering a long running process
"""

import os
import logging as flog   # Flask app logs
from flask import Flask, request, jsonify, abort, make_response, Response
import json   # For parsing and creating json


# My modules
from .greeting_blueprint import greeting_blueprint

here = os.path.dirname(__file__)

flog.basicConfig(level=flog.DEBUG)

app = Flask(__name__, static_url_path='')

# Add blueprint views 
app.register_blueprint(greeting_blueprint, url_prefix='/pages')  # expose route: /greeting

# Log the rules registered on the application, showing the blueprints
flog.info(f"app.url_map:{app.url_map}")

# ---------------------------------------------
# stations Utility functions
# ---------------------------------------------
def load_stations():
  """Read stations from storage"""
  return {}

@app.route('/')
def index():
  return "Hello World!"

#------------------------
# stations routes
#------------------------
@app.route('/stations', methods=['GET'])
def stations_get():
  """Get stations 
  :return: Json List of Dict
  """
  flog.debug("Called stations_get")
  try:
    response = load_stations()
    flog.info(f"stations:{response}")
    http_code = 200
  except Exception as e:
    response = { 'status': 'failure', 'error': str(e) }
    flog.error(f"error:{response}")
    http_code = 400
 

  return Response(
    json.dumps(
        response, sort_keys=True, indent=4, separators=(',', ': ')
    ),
    mimetype="application/json"
  ), http_code 

# TODO:
#@app.route('/stations/', methods=['GET'])
#@app.route('/stations', methods=['POST'])
#@app.route('/stations/<station_id>'  , methods=['PUT'])
#@app.route('/stations/<station_id>'  , methods=['DELETE'])
#------------------------
