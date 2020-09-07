#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
gunicorn config.asgi:application -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --chdir=/app