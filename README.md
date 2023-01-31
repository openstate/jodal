# jodal

jodal is het JOurnalistiek DAshboard Lokaal.


## Get started

1. `# clone the repo and chdir to there`
2. `cd backend && cp config.py.example config.py && cp config.yaml.example config.yaml`
3. `# Edit config.py and config.yaml accordingly to what you want`
2. `cd ../docker`
3. `docker-compose  up -d`
4. `docker exec jodal_backend_1 ./manage.py elasticsearch put_templates`
5. `docker exec jodal_backend_1 alembic upgrade head`

In development mode you can run `./bin/dev.sh` from the base directory, which will launch
the development environment.

To access the local development environment, add the following in `/etc/hosts`:

```
127.0.0.1	api.jodal.nl users.jodal.nl www.jodal.nl app.jodal.nl
```

Then you can go to `http://app.jodal.nl` preferably in a private window, because of HSTS parameters on the live setup.

# deployment

Open Overheidsdata uses Fabric for deployment. Run `fab deploy`.

# migrations

Open Overheidsdata uses [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for migrations

## migrate all up to the latest

`docker exec jodal_backend_1 alembic upgrade head`

## rollback

`docker exec jodal_backend_1 alembic downgrade -1`

## create a migration

`docker exec jodal_backend_1 alembic revision -m "create account table"`

# adding data

Open Overheidsdata runs several scrapers, in the `jodal_backend_1` container. Run the floowing steps to get started:

1. `docker exec jodal_backend_1 ./mana ge.py scrapers locations`
2. `docker exec jodal_backend_1 ./mana ge.py scrapers openspending -f 2021-01-01`
3. `docker exec jodal_backend_1 ./mana ge.py scrapers poliflw -f 2021-01-01`
4. `docker exec jodal_backend_1 ./mana ge.py scrapers obv -f 2021-01-01`

# contact

Send an email to breyten@openstate.eu
