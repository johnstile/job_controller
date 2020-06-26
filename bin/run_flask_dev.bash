#!/usr/bin/env bash
set -e  # fail on errors

echo "[>>]  Starting Flask directory on developmnet system"

echo "[>>]  Activate Isolated python" 
. venv/bin/activate

echo "[>>]  Run app in Flask development server" 
FLASK_APP="src.web.myapp:app" flask run

