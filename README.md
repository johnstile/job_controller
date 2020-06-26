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
setup_python_venv.bash : In development, setup isolated python 
run_flask_dev.bash     : In development, directlry run flask
```
