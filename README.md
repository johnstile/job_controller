# Job Controller 
```.
This is a Job controller sutie
- General idea: web interfaceto run process on remote hosts
```
## Architecture
```.
- Services are run in Docker containers
- docker-composer will start the containers.
- Description of Services:
- Nginx    : Proxy requests to static content, redis, and flask
- Gunicorn : WSGI runner, serving Flask app
- Flask    : Backend app handles job actions, logs, and talks to redis
- Redis    : RedisRQ job queue
```
## Scripts:
```.
bin/setup_python_venv.bash : In development, setup isolated python 
bin/run_flask_dev.bash     : In development, directlry run flask
setup.py                   : Packages src python into pip installable package
```
## Configs:
```.
Flask config files:
- dev_flask.cfg  : Development
- flask.cfg          : Prodiction
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
