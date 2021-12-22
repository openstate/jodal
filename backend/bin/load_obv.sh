#!/bin/bash
CUR_YEAR=`date '+%Y'`
for y in `seq 2010 $CUR_YEAR`;
do
  for m in `seq 1 11`;
  do
    nm=`expr $m + 1`
    ./manage.py scrapers obv -f "$y-$m-01" -t "$y-$m-15" -o $1
    ./manage.py scrapers obv -f "$y-$m-15" -t "$y-$nm-01" -o $1
  done
done
