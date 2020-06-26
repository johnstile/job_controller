#!/usr/bin/env bash
echo "#------------------------------"
echo "# Setup one Python venv for all parts"
echo "#------------------------------"

# Create isolated python install 
if [ ! -d "venv" ]; then
  virtualenv --version
  if [ $? -ne 0 ]; then
    echo "ERROR: check virtualenv install"
    exit 1
  fi
  python3 --version
  if [ $? -ne 0 ]; then
    echo "ERROR: check python3 install"
    exit 1
  fi
  virtualenv -p python3 venv
  if [ $? -ne 0 ]; then
    echo "ERROR: virtualenv setup failed"
    exit 1
  fi
fi
. venv/bin/activate
pip3 install -r pip_requirements.txt
if [ $? -ne 0 ]; then
  echo "ERROR: pip install failed"
  exit 1
fi
deactivate
echo "---------------------------------"
echo "Setup complete"
echo "---------------------------------"
