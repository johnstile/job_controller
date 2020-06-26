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
## Build:
```.
- Run dockerd on host OS
- Create Docker Volumes for logs and redis 
  docker volume create job_logs
- Build containers and start them
  docker-compose up --build
- Test: http://127.0.0.1/
- Under Hamberger menu, Edit Stations
  Add sations
- Under Hamberger menu, Run Test
  Fill in the form, and click run
```
## WEB APP Structure:
```.
The Client is written in React, using Context for state
 Location: nginx/react
The Server is written in Python with Flask
 Location: src/web 
The Worker is written in Python 
 Location: src/util
```
## WEB API:
setup_python_venv.bash - For development create a python virtualenv.
setup.py - Run by Dockerfiles, creating a Python *.whl file, installed in the Containers.
## WEB API:
```.
WIP:
```
