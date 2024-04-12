#!/bin/bash

export DJANGO_SETTINGS_MODULE=app.settings

# Migrate database
poetry run python manage.py migrate

# Start the workers
poetry run celery -A workers.worker_app worker --loglevel=INFO --concurrency=5