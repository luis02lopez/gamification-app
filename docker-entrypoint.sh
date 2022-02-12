#!/bin/bash

set -e

echo "Scan models"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

exec "@"