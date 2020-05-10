from .dev_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['django-env.eba-bqurfhwn.us-west-2.elasticbeanstalk.com']

CORS_ORIGIN_WHITELIST = ['https://master.d1tifnnvu21b6i.amplifyapp.com/']
CSRF_TRUSTED_ORIGINS = ['https://master.d1tifnnvu21b6i.amplifyapp.com/']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
