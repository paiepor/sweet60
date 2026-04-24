web: gunicorn sweet60_project.wsgi --log-file -
release: python manage.py migrate && python manage.py create_admin
