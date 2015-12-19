FROM ubuntu:15.10
MAINTAINER Martin Helmich <kontakt@martin-helmich.de>

RUN apt-get update

RUN apt-get install -y nginx

RUN rm -f /etc/nginx/sites-enabled/*
ADD site.conf /etc/nginx/sites-enabled/typo3.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

EXPOSE 80

CMD "chown www-data. /var/run/php/php-fpm.sock && nginx"
