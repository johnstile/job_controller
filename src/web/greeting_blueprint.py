""" Intial hellow route 
REF: https://realpython.com/flask-blueprint/
"""

from flask import Blueprint

# object name                 (<decor_name>       , <import_name>)
greeting_blueprint = Blueprint('greeting_blueprint', __name__)

# Add a View
@greeting_blueprint.route('/greeting')
def index():
    return "Welcome to my app"


