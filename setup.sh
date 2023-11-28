#!/bin/sh
docker exec jodal_backend_1 alembic upgrade head
docker exec jodal_backend_1 ./manage.py elasticsearch put_templates
