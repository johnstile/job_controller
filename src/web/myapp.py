#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for job controller
Using blueprint for API version
"""

import os
import logging
from flask import Flask, jsonify, Response, request, abort
from flask_cors import CORS  # To allow Swagger and other things to work
import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, jwt_optional, get_jwt_claims
)

# My API Versions
from .api_v1_blueprint import jwt, api_v1_blueprint


here = os.path.dirname(__file__)
app = Flask(__name__, static_url_path='')

jwt = JWTManager()
jwt.init_app(app)

# Register root logger, so blueprint can send logs
# Log Level:  basicConfig: my python, werkzeug: all requests
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app.config.from_pyfile(os.path.join(here, 'flask.cfg'))

# we have some cross domain stuff behind nginx
CORS(app)

# Expose API under /V1/
# e.g. /V1/stations
app.register_blueprint(api_v1_blueprint, url_prefix='/V1')


@app.route('/')
def index():
    return "Hello Job Controller!!"


@app.route('/echo_request')
def echo_request():
    """API independent route to view request header info"""
    return jsonify(dict(request.headers))


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0')
