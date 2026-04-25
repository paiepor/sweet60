web: gunicorn sweet60_project.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
release: python manage.py migrate && python manage.py create_admin
