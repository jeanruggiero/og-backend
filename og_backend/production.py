from .settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = []
CSRF_TRUSTED_ORIGINS = []
CSRF_COOKIE_SECURE = True