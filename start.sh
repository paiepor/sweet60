#!/bin/bash
set -e
echo "=== Starting Sweet Sixty ==="
echo "PORT=$PORT"
python manage.py migrate --noinput
echo "=== Migration done, starting gunicorn on port ${PORT:-8000} ==="
exec gunicorn sweet60_project.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --timeout 120
