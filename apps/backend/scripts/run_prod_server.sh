#!/bin/bash

# Migrate database
poetry run python manage.py migrate

# Start server with gunicorn
poetry run gunicorn app.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000