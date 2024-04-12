#!/bin/bash

export DJANGO_SETTINGS_MODULE=app.settings

# Migrate database
poetry run python manage.py migrate

# Start the workers
poetry run watchmedo auto-restart -d . -p '*.py' -R -- celery -- -A workers.worker_app worker --loglevel=DEBUG --concurrency=5

