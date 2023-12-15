#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --no-input

gunicorn --bind 0.0.0.0:8000 bot_admin.asgi -w 4 -k uvicorn.workers.UvicornWorker
