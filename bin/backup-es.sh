#!/bin/bash
ES_LATEST=`sudo docker exec jodal_backend_1 curl -s 'http://elasticsearch:9200/_snapshot/ood_backups/_all?pretty' |jq -r '.snapshots[-1] |.snapshot |@text'`
sudo docker exec jodal_backend_1 curl -XPUT 'http://elasticsearch:9200/_snapshot/ood_backups/\%3Cbackup1-\%7Bnow\%2Fd\%7D\%3E'
sudo docker exec jodal_backend_1 curl -XDELETE "http://elasticsearch:9200/_snapshot/ood_backups/$ES_LATEST"
