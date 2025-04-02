#!/bin/bash

CONTAINER="jodal_backend_1"

# Get the name of the latest backup
ES_LATEST=`sudo docker exec $CONTAINER curl -s 'http://elasticsearch:9200/_snapshot/ood_backups/_all?pretty' |jq -r '.snapshots[-1] |.snapshot |@text'`

# Create a name for the new backup
SNAPSHOT_NAME="backup1_$(date +%Y%m%d%H%M)"

# Create a new backup
sudo docker exec $CONTAINER curl -XPUT "http://elasticsearch:9200/_snapshot/ood_backups/$SNAPSHOT_NAME?wait_for_completion=true"

# Delete the latest backup
sudo docker exec $CONTAINER curl -XDELETE "http://elasticsearch:9200/_snapshot/ood_backups/$ES_LATEST"
