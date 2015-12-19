FROM ubuntu:15.10
MAINTAINER Martin Helmich <kontakt@martin-helmich.de>

RUN apt-get update

RUN apt-get install -y software-properties-common
RUN locale-gen en_US.UTF-8

RUN apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0x5a16e7281be7a449 && \
    add-apt-repository 'deb http://dl.hhvm.com/ubuntu wily main' && \
    apt-get update

RUN apt-get install -y \
    hhvm

VOLUME /var/run/php

CMD ["/usr/bin/hhvm", \
    "-m", "server", \
    "-d", "hhvm.server.file_socket=/var/run/php/php-fpm.sock", \
    "-d", "hhvm.server.type=fastcgi"]
