#!/bin/bash

CONTAINER="jodal-backend-1"

# Get the name of the latest backup
LAST_SNAPSHOT=`sudo docker exec $CONTAINER curl -s 'http://elasticsearch:9200/_snapshot/ood_backups/_all?pretty' |jq -r '.snapshots[-1] |.snapshot |@text'`

# Create a name for the new backup
NEW_SNAPSHOT="backup1_$(date +%Y%m%d%H%M)"

# Create a new backup and capture the HTTP status code
HTTP_STATUS=$(sudo docker exec $CONTAINER curl -s -o /dev/null -w "%{http_code}" -XPUT "http://elasticsearch:9200/_snapshot/ood_backups/$NEW_SNAPSHOT?wait_for_completion=true")

# Check if the backup creation was successful (HTTP 200 or 201)
if [[ "$HTTP_STATUS" -eq 200 || "$HTTP_STATUS" -eq 201 ]]; then
  echo "Backup created successfully with name: $NEW_SNAPSHOT."
  echo "Deleting the previous backup: $LAST_SNAPSHOT..."
  # Delete the latest backup
  sudo docker exec $CONTAINER curl -s -o /dev/null -XDELETE "http://elasticsearch:9200/_snapshot/ood_backups/$LAST_SNAPSHOT"
else
  echo "Backup creation failed with status code $HTTP_STATUS. Not deleting the previous backup."
  exit 1
fi
