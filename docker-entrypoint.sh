#!/bin/bash

set -e

echo "Scan models"
python manage.py makemigrations --noinput
python manage.py makemigrations app --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput
python manage.py migrate app --noinput


#Superuser
if $DJANGO_CREATE_SUPERUSER; then
    python manage.py createsuperuser --email=llopez25@cuc.edu.co --no-input
fi

exec "$@"