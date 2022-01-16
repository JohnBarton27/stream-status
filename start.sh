#!/bin/bash

cd ~/Documents/stream-status
source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
python streamstatus/main.py

