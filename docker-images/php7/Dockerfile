FROM ubuntu:15.10
MAINTAINER Martin Helmich <kontakt@martin-helmich.de>

RUN apt-get update

RUN apt-get install -y software-properties-common
RUN locale-gen en_US.UTF-8

# add-apt-repository is too fucking stupid to handle UTF8 without any
# special hassle. Ugh.
#   http://askubuntu.com/questions/490468/add-apt-repository-throws-python-error
RUN LC_ALL=en_US.UTF8 add-apt-repository ppa:ondrej/php-7.0 && \
    apt-get update

RUN apt-get install -y \
    php7.0-fpm \
    php7.0-mysql

VOLUME /var/run/php

ADD fpm-pool.conf /etc/php/7.0/fpm/pool.d/typo3.conf
RUN rm /etc/php/7.0/fpm/pool.d/www.conf

CMD ["/usr/sbin/php-fpm7.0", "-F"]
