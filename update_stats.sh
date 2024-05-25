#!/bin/bash
source www/python/venv/bin/activate
cd www/python/src

dt=$(date '+%d/%m/%Y-%H:%M:%S')

# Runs the update commands, and logs their results in case of success and failure
(python gen_stats.py 2>&1 && echo "$dt Stats Update Job ran successfully") || (echo "==============================================" && echo "$dt Stats Update Job failed")
