# Job Controller 
```.
web interface to run long-running process on networked hosts
```
## Quick Start
```.
Start dockerd: 
 For sysv init:
 sudo service systemd restart
 For Systemd
 sudo systemctl start docker
 For OpenRc
 sudo /etc/init.d/docker start


Start development container environment: 
  docker-compose -f  docker-compose-dev.yml up --build
  NOTE: Containers mount this directory, so changes don't require restart
-OR-
Star production container environment: 
  docker-compose up --build

Stop container minions:
  docker-compose stop

List running containers:
  docker container list -a

List images:
  docker image list -a

Debugging: connect to running container:
  docker exec -it <container name> sh

Inspect Dockerd resource management:
  docker system df -v

List Running services:
  docker system ps 

List Dead and Running services:
  # Handy if you want to run and connect to a dead container
  docker system ps -a

```
## Container URLs
```.
Nginx   : Routes all external requests 
 URL: http://127.0.0.1

UI App   : React front end 
 URL: http://127.0.0.1/

Backend App   : Flask app, talks to Redis, JobQueue, etc
 e.g. http://127.0.0.1/echo_request 
 e.g. http://127.0.0.1/V1/version

Swagger-ui  : To test backend via API (reads swagger.yaml)
 URL: http://127.0.0.1/api/swagger-ui/

Swagger-editor : Used to edit swagger.yaml
 URL: http://127.0.0.1/api/swagger-editor

```
## React Local Development 
```.
cd react
npm install
npm run start
Access via: http://127.0.0.1:8080

```
## Flask Local Development  (non-docker)
```.
Initial setup, create isolated python environment
 sudo apt-get install python3-venv
 python3 -m venv venv
 . venv/bin/activate
 pip install -r pip_requirements.txt

IDE setup: VS Code:
Launch VS Code:
1. Install extension: settings sync
 -> I setup a private gist, and configured plugin to use it.
 -> This should install all the Extensions (python, pylint, react, eslint)
 --> The gist is named "cloudSettings"
 ---> TODO: Test simulated sharing with a Team Mate, and stor in this repo
 ---> Access settings: <ctrl>-<shift>-p, type: sync settings 

2. File -> Open Directory -> <top of working copy directory> 
  Open src/web/myapp.py (this activates the python plugin)
  Bottom blue bar should show the isolated python interpreter 

3. During Initial project setup, I created a run config (.vscode/launch.json)
  Steps followed:
    Click Bug tab on the left
    Run-> Open Configurations -> Flask -> Enter path to flask app: src/web/myapp.py
      Creates .vscode/launch.json
  
  To run on local flask server: 
    Run -> Start without debugging
    This launches flask dev server on http://127.0.0.1:5000/
    In a browser visit: http://127.0.0.1:5000/echo_request

  To run debug on local flask server: 
    Add break point to some route, by clicking to the right of line number.
      (e.g. src/web/myapp.py, in echo_request(), next to the return. )
    Run -> Start Debugging
    This launches flask dev server on http://127.0.0.1:5000/
    In a browser visit: http://127.0.0.1:5000/echo_request
    You should see the break point hit, and can inspect. 
```
## Architecture
```.
Description of Services (containers):
- Nginx    : Proxy requests to static content, Redis, and Flask
- Gunicorn : WSGI runner, serving Flask app
- Flask    : Backend app handles job actions, logs, and talks to Redis
- Redis    : Some persistent storage and RedisRQ job queue
```
## Scripts:
```.
bin/setup_python_venv.bash : In development, setup isolated python 
bin/run_flask_dev.bash  : In development, run flask server directly
setup.py  : Packages python source into wheel file for pip install
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
- Dockerfile.swagger-editor : Run Swagger-edit
- Dockerfile.web         : Run setup.py and install into Green Unicorn image
- Dockerfile.nginx       : Run Nginx and proxy to Green Unicorn and Swagger-ui
```
## WEB APP Structure:
```.
App state in react/context
App components in react/components
Project files:
 .eslintrc.json
 package.json
 package-lock.json
 webpack.config.js

