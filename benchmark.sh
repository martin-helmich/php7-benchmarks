#!/bin/bash

CMS="${1}"
PRODUCTS="php5 php7 hhvm"
CONCURRENCIES="1 10 20 50 100 200 300 400 500"
RAMPUPTIME=3

[ -z "${CMS}" ] && { echo "No CMS parameter set!" >&2 && exit 1 ; }
[ ! -d "${CMS}" ] && { echo "Directory ${CMS} does not exist" >&2 && exit 1 ; }

COMPOSE="docker-compose -f ${CMS}/docker-compose.yml"

function die() {
  echo "${1}" >&2
  exit 1
}

#docker-compose stop
#docker-compose rm php5fpm php7fpm hhvm php5nginx php7nginx hhvmnginx
#docker-compose up -d

#sleep 5

${COMPOSE} stop

for PRODUCT in $PRODUCTS ; do
  echo "Benchmarking $PRODUCT..."
  echo "You have ${RAMPUPTIME}s to abort."

  sleep ${RAMPUPTIME}

  ${COMPOSE} up -d --no-color ${PRODUCT}nginx \
    || die "Could not start Docker containers for ${CMS} with ${PRODUCT}!"

  sleep 3

  #docker-compose up -d --no-color ${PRODUCT}nginx
  #sleep 10
  IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' ${CMS}_${PRODUCT}nginx_1)

  for C in $CONCURRENCIES ; do
    DESCRIPTION="${CMS}-${PRODUCT}-c${C}"
    #docker run --rm --link ${CMS}_${PRODUCT}nginx_1:target -v ${PWD}:/work ${CMS}_siege -r 200 -c ${C} --log=/work/${CMS}.csv -m ${DESCRIPTION} http://target
    siege -b -r 200 -c $C --log=stats-${CMS}.csv -m ${DESCRIPTION} http://${IP}/
  done

  ${COMPOSE} stop
  #docker-compose stop
done
