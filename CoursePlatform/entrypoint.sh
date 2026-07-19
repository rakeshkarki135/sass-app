#!/bin/sh

#Exit immediately if a command exits with a non-zero status
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn Server..."
exec gunicorn apps.CoursePlatform.wsgi:application --bind 0.0.0.0:8000
# exec "$@" to run from dockerfile command 