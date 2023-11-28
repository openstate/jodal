# jodal

jodal is het JOurnalistiek DAshboard Lokaal.


## Get started

1. `# clone the repo and chdir to there`
2. `cd backend && cp config.py.example config.py && cp config.yaml.example config.yaml`
3. `# Edit config.py and config.yaml accordingly to what you want`
2. `cd ../docker`
3. `docker-compose  up -d`
4. `cd ..`
5. `./setup.sh`
6. `docker exec -it jodal_backend_1 ./manage.py scrapers locations`

In development mode you can run `./bin/dev.sh` from the base directory, which will launch
the development environment.

To access the local development environment, add the following in `/etc/hosts`:

```
127.0.0.1	api.jodal.nl users.jodal.nl www.jodal.nl app.jodal.nl
```

Then you can go to `http://app.jodal.nl` preferably in a private window, because of HSTS parameters on the live setup.

## Installing FusionAuth

1. Go to `http://localhost:9011/`
2. Make an admin account
3. Complete the steps on the main DAshboard
  1. Make an application (for example 'jodal')
    1. Login ap config:
      - Require an API key: 	Yes
      - Generate Refresh Tokens: 	No
      - Enable JWT refresh: 	No
      - Passwordless: yes
    2. Authentication tokens: no
    3. JWT Enabled: Yes
    4. Self serice registration:
       - Enabled: Yes
       - Require password confirmation: Yes
       - Fields:
    5. OAuth config:
      - Require authentication: 	Yes
      - Generate Refresh Tokens: 	Yes
      - Logout URL: 	https://app.jodal.nl/
      - Logout behavior: 	All applications
      - Authorized origins: 	–
       Authorized redirects: 	https://api.jodal.nl/users/simple/callback, http://localhost:8080/api/2/sessions/callback, https://aleph.openstate.eu/api/2/sessions/callback
      - Enabled grants: 	Authorization Code, Refresh Token
    6. SAML:
      - Enabled: 	No
    7. Roles:
  2. Generate an api key for use with the jodal application
  3. Settings
   1. Cors: Enabled
  4. copy the client id and secret from the application to `backend/config.py`
  5. copy the api key to `backend/config.py`
  6. restart backend and api container
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
