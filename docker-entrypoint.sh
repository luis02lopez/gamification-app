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
python manage.py createsuperuser --username=admin --email=l_y02@hotmail.com --no-input

exec "$@"