#!/bin/bash

set -e

echo "Scan models"
python manage.py makemigrations 
python manage.py makemigrations app

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
python manage.py migrate app


#Superuser
if $DJANGO_CREATE_SUPERUSER; then
    python manage.py createsuperuser --email=llopez25@cuc.edu.co --no-input
fi

exec "$@"