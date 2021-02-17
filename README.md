# jodal

jodal is het JOurnalistiek DAshboard Lokaal.


## Get started

1. `# clone the repo and chdir to there`
2. `cd docker`
3. `docker-compose  up -d`
4. `docker exec jodal_backend_1 ./manage.py elasticsearch put_templates`

In development mode you can run `./bin/dev.sh` from the base directory, which will launch
the development environment. You can then go to http://localhost/ in your browser.

# migrations

Jodal uses [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for migrations

## migrate all up to the latest

`docker exec jodal_backend_1 alembic upgrade head`

## rollback

`docker exec jodal_backend_1 alembic downgrade -1`

# contact

Send an email to breyten@openstate.eu
