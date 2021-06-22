#!/bin/bash
#./manage.py scrapers openspendingcache $* |xargs -n 1 -I X curl -s "http://api-jodal:5000/documents/download/openspending/X" 2>/dev/null >cache/openspending/I.json
./manage.py scrapers openspendingcache $* 2>/dev/null |while read -r line;
do
  if [ ! -s "./cache/openspending/$line.json" ];
  then
    echo "$line";
    curl -s "http://api-jodal:5000/documents/download/openspending/$line?format=json" 2>/dev/null >/dev/null
  fi
done
