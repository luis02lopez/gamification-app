#!/bin/bash

set -e

echo "Scan models"
python manage.py makemigrations 
python manage.py makemigrations app

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
python manage.py migrate app

exec "$@"