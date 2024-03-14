#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --no-input

celery -A bot_admin worker --beat --scheduler django --loglevel=info --detach

gunicorn bot_admin.wsgi:application --bind 0.0.0.0:8000
