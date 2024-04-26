from .settings import *
import os

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['APPLICATION_DOMAIN']] if 'APPLICATION_DOMAIN' in os.environ else []

CSRF_TRUSTED_ORIGINS = [f"https://{os.environ['APPLICATION_DOMAIN']}"] if 'APPLICATION_DOMAIN' in os.environ else []

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["POSTGRES_DB"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
        'HOST': os.environ["POSTGRES_HOST"],
        'PORT': '',
    }
}
