# Bron

alle overheidsdata — monitor, filter, stuur door.


## Get started

How to setup a local development environment:

1. `git clone git@github.com:openstate/jodal.git`
2. `cd backend && cp config.py.example config.py && cp config.yaml.example config.yaml`
3. Edit `config.py` and `config.yaml` accordingly to what you want, not strictly necessary`
5. Edit `fa-kickstart/kickstart.json`, esp. the part where it creates an account
9. `./bin/dev.sh`
8. `./setup.sh`
10. `docker exec -it jodal_backend_1 ./manage.py scrapers locations`
10. `docker exec -it jodal_backend_1 ./manage.py scrapers cvdr` and other scrapers

To access the local development environment, add the following in `/etc/hosts` on Linux or `/Windows/System32/drivers/etc/hosts` on Windows:

```
127.0.0.1	api.bron.live app.bron.live heritrix.bron.live bron.live www.bron.live users.bron.live
```

Then you can go to `http://app.bron.live` preferably in a private window, because of HSTS parameters on the live setup.

You can quickly login using a link like `http://api.bron.live/users/login?email=bje@dds.nl&password=blatenblaten`

# deployment

Bron uses Fabric for deployment. Run `fab deploy`.

# migrations

Bron uses [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for migrations

## migrate all up to the latest

`docker exec jodal_backend_1 alembic upgrade head`

## rollback

`docker exec jodal_backend_1 alembic downgrade -1`

## create a migration

`docker exec jodal_backend_1 alembic revision -m "create account table"`

# adding data

Bron runs several scrapers, in the `jodal_backend_1` container. Run the floowing steps to get started:

1. `docker exec jodal_backend_1 ./manage.py scrapers locations`
2. `docker exec jodal_backend_1 ./manage.py scrapers openspending -f 2021-01-01`
3. `docker exec jodal_backend_1 ./manage.py scrapers poliflw -f 2021-01-01`
4. `docker exec jodal_backend_1 ./manage.py scrapers obv -f 2021-01-01`

# contact

Send an email to quinten@openstate.eu
