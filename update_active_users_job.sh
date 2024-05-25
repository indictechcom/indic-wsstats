#!/bin/bash
source www/python/venv/bin/activate
cd www/python/src

dt=$(date '+%Y%m')

# Runs the update commands, and logs their results in case of success and failure
(python active_user.py 2>&1 && echo "$dt Active Users Job ran successfully") || (echo "==============================================" && echo "$dt Active Users Job failed")
