from .settings import *
import os

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['APPLICATION_DOMAIN']] if 'APPLICATION_DOMAIN' in os.environ else []

DEBUG = False
