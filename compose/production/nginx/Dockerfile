FROM nginx:1.17.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -yq --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY ./compose/production/nginx/includes/ /etc/nginx/includes/
COPY ./compose/production/nginx/conf.d/ /etc/nginx/conf.d/


