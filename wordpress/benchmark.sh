#!/bin/bash

PRODUCTS="php5 php7 hhvm"
CONCURRENCIES="1 10 20 50 100 200 500"

for PRODUCT in $PRODUCTS ; do
  echo "Benchmarking $PRODUCT..."

  IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' wordpress_${PRODUCT}nginx_1)
  for C in $CONCURRENCIES ; do
    DESCRIPTION="${PRODUCT}-c${C}"
    siege -b -r 200 -c $C --log=stats.csv -m ${DESCRIPTION} http://${IP}
  done
done
