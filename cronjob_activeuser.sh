#!/bin/sh
source ~/crontab/venv/bin/activate
cd ~/www/python/src
python3 active_user.py $(date '+%Y%m')