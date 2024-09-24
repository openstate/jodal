# jodal

jodal is het JOurnalistiek DAshboard Lokaal.


## Get started

How to setup a local development environment:

1. `git clone git@github.com:openstate/jodal.git`
2. `cd backend && cp config.py.example config.py && cp config.yaml.example config.yaml`
3. `# Edit config.py and config.yaml accordingly to what you want, not strictly necessary`
4. `cd ../docker`
5. `Edit fa-kickstart/kickstart.json, esp. the part where it creates an account`
6. `docker-compose  up -d backend mysql elasticsearch`
7. `cd ..`
9. `./bin/dev.sh`
8. `./setup.sh`
10. `docker exec -it jodal_backend_1 ./manage.py scrapers locations`

To access the local development environment, add the following in `/etc/hosts`:

```
127.0.0.1	api.bron.live app.bron.live heritrix.bron.live bron.live www.bron.live users.bron.live
```

Then you can go to `http://app.jodal.nl` preferably in a private window, because of HSTS parameters on the live setup.

You can quickly login using a link like `http://api.bron.live/users/login?email=bje@dds.nl&password=blatenblaten`

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
