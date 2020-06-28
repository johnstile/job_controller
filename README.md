# Job Controller 
```.
This is a Job controller suite
- General idea: web interface to run process on remote hosts
```
## Start it up 
```.
Development:
 docker-compose -f  docker-compose-dev.yml  up --build
Production:
 docker-compose up --build
```
## URLs
```.
http://127.0.0.1:81/#/
  Swagger-ui
  Uses swagger.json
  Enables user to test the API server side
http://127.0.0.1/v1
  Flask APP
  Directly acces the backend API
  
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
- Redis    : RedisRQ job queue
```
## Scripts:
```.
bin/setup_python_venv.bash : In development, setup isolated python 
bin/run_flask_dev.bash     : In development, directly run flask
setup.py                   : Packages src python into pip install-able package
```
## Configs:
```.
Flask config files:
- dev_flask.cfg  : Development
- flask.cfg          : Production
How used:
- src/web/myapp.py looks for flask app.conf in 'flask.cfg'
- Dockerfile.web copies one of these files to src/web/flask.cfg
- setup.py includes  'flask.cfg' in the package whl file
```
## Docker:
```.
Star: docker-compose up --build
Stop: docker-compose stop
Files:
- docker-compose.yml     : Runs Docker file, sets up ports, volumes, etc
- Dockerfile.swagger-ui  : Run Swagger-ui to test API
- Dockerfile.web         : Run setup.py and install into Green Unicorn image
```
