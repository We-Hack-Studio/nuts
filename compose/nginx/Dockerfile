FROM nginx:1.17.1

RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY ./compose/nginx/includes/ /etc/nginx/includes/
COPY ./compose/nginx/conf.d/ /etc/nginx/conf.d/


