toolforge jobs run stats-update --command www/python/src/update_stats.sh --image python3.11 --schedule "@daily" -o www/python/src/jobs.log
toolforge jobs run active-users-update --command www/python/src/update_active_users_job.sh --image python3.11 --schedule "@monthly" -o www/python/src/jobs.log
