#!/bin/bash
set -e
echo "=== Starting Sweet Sixty ==="
echo "PORT=$PORT"
python manage.py migrate --noinput
mkdir -p staticfiles
python manage.py collectstatic --noinput --clear
echo "=== Starting daphne on port ${PORT:-8000} ==="
exec daphne -b 0.0.0.0 -p ${PORT:-8000} sweet60_project.asgi:application
