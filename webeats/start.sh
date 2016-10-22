#!/bin/bash

echo "collect Static"
python manage.py collectstatic --noinput
echo "init db"
python manage.py migrate
echo "create superuser"
python manage.py initadmin
# Start Gunicorn process
echo "Starting Gunicorn"
exec gunicorn webeats.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3
