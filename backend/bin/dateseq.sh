#!/usr/bin/env bash
BY=$1
EY=$2
for y in `seq $BY $EY`;
do
  for i in `seq 0 365`;
  do
    date -d "$y-01-01 $i days" +%Y-%m-%d;
  done;
done;
