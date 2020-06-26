#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Flask App for triggering a long running process
"""

import os
import logging as flog  # Flask app logs
from flask import Flask, request, jsonify, abort, make_response, Response

from .greeting_blueprint import greeting_blueprint

here = os.path.dirname(__file__)

flog.basicConfig(level=flog.DEBUG)

app = Flask(__name__, static_url_path='')

# Add blueprint views 
app.register_blueprint(greeting_blueprint)

@app.route('/')
def index():
    return "Hello World"
