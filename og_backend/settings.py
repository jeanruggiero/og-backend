from .dev_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['ocularize-backend.us-west-2.elasticbeanstalk.com', 'api.ocularize.com']

CORS_ORIGIN_WHITELIST = ['https://ocularize.com', 'https://www.ocularize.com', 'https://staff.ocularize.com']
CSRF_TRUSTED_ORIGINS = ['https://app.ocularize.com']

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}
