# Procfile for Render deployment
# Specifies commands to run on Render

# Release phase - Run migrations before deployment
release: python manage.py migrate

# Web process - Run Django app with Gunicorn
web: gunicorn core.wsgi
