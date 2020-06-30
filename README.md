# Job Controller 
```.
web interface to run long-running process on networked hosts
```
## Quick Start
```.
Start dockerd: 
  sudo /etc/init.d/docker start
Start development environment: 
  docker-compose -f  docker-compose-dev.yml up --build
  NOTE: Containers mount this directory, so changes don't require restart
-OR-
Star production environment: 
  docker-compose up --build

Stop daemons:
  docker-compose stop

List running containers:
  docker container list
```
## URLs
```.
Swagger-ui  : Used to test Flask (reads swagger.yaml)
 URL: http://127.0.0.1/api/swagger-ui/

Flask App   : Backend, talks to Redis, JobQueue, etc
 URL: http://127.0.0.1
 e.g. http://127.0.0.1/echo_request 
 e.g. http://127.0.0.1/V1/version

```
## React Development 
```.
cd react
npm install
npm run start

```
## Architecture
```.
Description of Services (containers):
- Nginx    : Proxy requests to static content, redis, and flask
- Gunicorn : WSGI runner, serving Flask app
- Flask    : Backend app handles job actions, logs, and talks to redis
- Redis    : Some persistant storage and RedisRQ job queue
```
## Scripts:
```.
bin/setup_python_venv.bash : In development, setup isolated python 
bin/run_flask_dev.bash  : In development, run flask server directly
setup.py  : Packages pyton source into wheel file for pip install
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
Files:
- docker-compose-dev.yml : Runs Docker fils, for development 
- docker-compose.yml     : Runs Docker files, sets up ports, volumes, etc
- Dockerfile.swagger-ui  : Run Swagger-ui to test API
- Dockerfile.web         : Run setup.py and install into Green Unicorn image
- Dockerfile.nginx       : Run Nginx and proxy to Green Unicorn and Swagger-ui
```
## WEB APP Structure:
```.
App state in react/context
App components in react/components
Projcect files:
 .eslintrc.json
 package.json
 package-lock.json
 webpack.config.js

