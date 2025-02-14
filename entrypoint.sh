#!/bin/bash

set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn homework_08.wsgi:application --bind 0.0.0.0:8000