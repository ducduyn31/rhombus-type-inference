#!/bin/bash

# Migrate database
poetry run python manage.py migrate

# Start Django development server
poetry run python manage.py runserver 0.0.0.0:8000