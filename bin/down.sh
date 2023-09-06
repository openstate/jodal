#!/bin/sh
FQPATH=`readlink -f $0`
BINDIR=`dirname $FQPATH`
cd $BINDIR/../docker
docker-compose -f docker-compose.yml -f docker-compose-dev.yml down 
cd -
