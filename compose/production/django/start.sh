#!/bin/sh

python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py migrate
gunicorn config.asgi:application -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --chdir=/app