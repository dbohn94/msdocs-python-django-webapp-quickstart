python manage.py migrate
celery -A quickstartproject worker --logfile celery.log &
celery -A quickstartproject beat -l info -S django --logfile celery-beat.log &
gunicorn --bind=0.0.0.0 --timeout 600 quickstartproject.wsgi
