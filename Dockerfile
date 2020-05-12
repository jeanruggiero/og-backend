FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends

COPY nginx.default /etc/nginx/sites-available/default

#RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#    && ln -sf /def/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/og_backend
RUN mkdir -p /etc/pki/tls/certs

COPY requirements.txt start-server.sh /opt/app/
COPY og_backend /opt/app/og_backend/og_backend
COPY intake /opt/app/og_backend/intake
COPY static /opt/app/og_backend/static

COPY server.crt /etc/pki/tls/certs
#COPY server.key /etc/pki/tls/certs

WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app

EXPOSE 443
STOPSIGNAL SIGTERM
CMD ["./start-server.sh"]
