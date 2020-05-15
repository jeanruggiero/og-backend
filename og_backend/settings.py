from .dev_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['optometricgroup.us-west-2.elasticbeanstalk.com', 'api.highlift.io', 'localhost', '127.0.0.1']

CORS_ORIGIN_WHITELIST = ['https://app.highlift.io']
CSRF_TRUSTED_ORIGINS = ['https://app.highlift.io']

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")