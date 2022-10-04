#!/usr/bin/env bash
BY=$1
EY=$2
for y in `seq $BY $EY`;
do
  for i in `seq 0 365`;
  do
    CVDR_DAY=`date -d "$y-01-01 $i days" +%Y-%m-%d;`
    ./manage.py scrapers cvdr -f "$CVDR_DAY" -t "$CVDR_DAY" -w updated_at
    sleep 1
  done;
done;
