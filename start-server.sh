#!/usr/bin/env bash

# Script to start nginx and gunicorn servers

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  (cd og_backend; python manage.py createsuperuser --no-input; python manage.py migrate)
fi

aws s3 cp s3://elasticbeanstalk-us-west-2-757222208482/certs/server.key /etc/pki/tls/certs/server.key

(cd og_backend; gunicorn og_backend.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"