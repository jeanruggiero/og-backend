from .dev_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['django-env.eba-bqurfhwn.us-west-2.elasticbeanstalk.com']

CORS_ORIGIN_WHITELIST = []
CSRF_TRUSTED_ORIGINS = []
