# Job Controller 
```.
This is a Job controller suite
- General idea: web interface to run process on remote hosts
```
## Quick Start
```.
Start Dev:
 docker-compose -f  docker-compose-dev.yml  up --build
-OR-
Star Prod:
 docker-compose up --build
```
## URLs
```.
Swagger-ui: http://127.0.0.1/api/swagger-ui/
 Uses swagger.yaml
 Use to test Flask 

Flask App: http://127.0.0.1
 e.g. http://127.0.0.1/echo_request 
 e.g. http://127.0.0.1/V1/version

```
## Architecture
```.
- Services are run in Docker containers
- docker-composer will start the containers (There are 2 docker-composer files (Dev,Prod))
-- docker-compose.yml      : Starts everything for production
-- docker-compose-dev.yml  : mounts this directory so changes do not require reload 
- Description of Services:
- Nginx    : Proxy requests to static content, redis, and flask
- Gunicorn : WSGI runner, serving Flask app
- Flask    : Backend app handles job actions, logs, and talks to redis
- Redis    : Some persistant storage and RedisRQ job queue
```
## Scripts:
```.
bin/setup_python_venv.bash : In development, setup isolated python 
bin/run_flask_dev.bash     : In development, run flask server directly
setup.py                   : Python setuptools script to package src dir into wheel file
```
## Configs:
```.
Flask config files:
- flask-dev.cfg  : Development
- flask.cfg      : Production
How they are used:
- The flask app (src/web/myapp.py) reads configs from flask.cfg
- Dockerfile.web copies one of these files to src/web/flask.cfg
- setup.py includes  'flask.cfg' in the whl package, which is 
  installed in the docker container. 
```
## Docker:
```.
Stop:      docker-compose stop
Files:
- docker-compose.yml     : Runs Docker file, sets up ports, volumes, etc
- Dockerfile.swagger-ui  : Run Swagger-ui to test API
- Dockerfile.web         : Run setup.py and install into Green Unicorn image
- Dockerfile.nginx       : Run Nginx and proxy to Green Unicorn and Swagger-ui
```
