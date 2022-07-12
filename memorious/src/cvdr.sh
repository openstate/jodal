#!/bin/sh
export ALEPHCLIENT_API_KEY=xxxx
export ALEPHCLIENT_HOST=https://aleph.openstate.eu
export CVDR_FOREIGN_ID=yyyy

cd /memorious
memorious run decentrale_regelgeving_recent
cd /crawlers/src
python3 load_decentrale_regelgeving.py -f $CVDR_FOREIGN_ID  -d /data/results/decentrale_regelgeving_recent -b 2 -s 5
#rm -fr /data/results/covid19/*
