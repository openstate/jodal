#!/bin/sh
FQPATH=`readlink -f $0`
BINDIR=`dirname $FQPATH`
cd $BINDIR/../docker
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d
sleep 5
docker exec -it jodal_node_1 npm run dev
cd -
