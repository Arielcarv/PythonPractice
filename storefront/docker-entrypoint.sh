#!/bin/bash

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8080 storefront.wsgi:application
