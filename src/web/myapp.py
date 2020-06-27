#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for job controller
Using blueprint for API version
"""

import os
from flask import Flask, jsonify, Response, request, abort
from flask_cors import CORS  # To allow Swagger and other things to work

# My API Versons
from .api_v1_blueprint import api_v1_blueprint


class StationsError(Exception):
    """Base Station Error"""
    status_code = 400


class StationsRequestError(StationsError):
    """Threat Stack request error."""


class StationsAPIError(StationsError):
    """Threat API Stack error."""


here = os.path.dirname(__file__)

app = Flask(__name__, static_url_path='')

app.config.from_pyfile(os.path.join(here, 'flask.cfg'))

# we have some cross domain stuff behind nginx
CORS(app)

# Expose API under /V1/
# e.g. V1 of  /stations is is under /V1/stations
app.register_blueprint(api_v1_blueprint, url_prefix='/V1')

@app.route('/')
def index():
    return "Hello Job Controller!!"

@app.route('/echo_request')
def echo_request():
    """API independent route to ensure things are working"""
    return jsonify(dict(request.headers))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0')
