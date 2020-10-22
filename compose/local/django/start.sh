#!/bin/sh

python manage.py compilemessages
python manage.py migrate
python manage.py setup_periodic_tasks
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --log-level debug --access-log
