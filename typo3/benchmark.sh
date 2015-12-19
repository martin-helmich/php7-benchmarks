#!/bin/bash

CMS="typo3"
PRODUCTS="php5 php7 hhvm"
CONCURRENCIES="1 10 20 50 100 200 300 400 500"

#docker-compose stop
#docker-compose rm php5fpm php7fpm hhvm php5nginx php7nginx hhvmnginx
#docker-compose up -d

#sleep 5

for PRODUCT in $PRODUCTS ; do
  echo "Benchmarking $PRODUCT..."

  sleep 10

  #docker-compose up -d --no-color ${PRODUCT}nginx
  #sleep 10
  IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' ${CMS}_${PRODUCT}nginx_1)

  for C in $CONCURRENCIES ; do
    DESCRIPTION="${CMS}-${PRODUCT}-c${C}"
    #docker run --rm --link ${CMS}_${PRODUCT}nginx_1:target -v ${PWD}:/work ${CMS}_siege -r 200 -c ${C} --log=/work/${CMS}.csv -m ${DESCRIPTION} http://target
    siege -b -r 200 -c $C --log=stats.csv -m ${DESCRIPTION} http://${IP}/
  done

  #docker-compose stop
done
