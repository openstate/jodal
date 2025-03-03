# Bron

Superpowers for journalists. Search through more than 2 million government documents in one place. Formerly known as Jodal.

Use Bron on [bron.live](https://bron.live) or keep reading to start local development.

## Getting started

Run the following commands to set up your development environment:
1. `git clone git@github.com:openstate/jodal.git`
2. `cd backend && cp config.py.example config.py && cp config.yaml.example config.yaml`
3. Edit `config.py` and `config.yaml` accordingly to what you want, not strictly necessary`
4. Edit `fa-kickstart/kickstart.json`, esp. the part where it creates an account
5. `./bin/dev.sh`
6. `./bin/setup.sh`
7. `docker exec -it jodal_backend_1 ./manage.py scrapers locations`
8. `docker exec -it jodal_backend_1 ./manage.py scrapers obv` and other scrapers

To access the local development environment, add the following in `/etc/hosts` on Linux or `/Windows/System32/drivers/etc/hosts` on Windows:

```
127.0.0.1	bron.live www.bron.live api.bron.live docs.bron.live users.bron.live
```

Then you can go to `http://bron.live`, preferably in a private window, because of HSTS parameters on the live setup. In development, changes made in `/frontend/` will be instantly visible in the browser, whereas other changes require a container restart, and when including new dependencies, a new image build as well.

## Architecture

Bron runs entirely through Docker Compose. This is configured in production using `/docker/docker-compose.yml` and overridden in development using `/docker/docker-compose-dev.yml`. Some parts of Bron are exposed to the web using Nginx, with configs in `/docker/nginx/` and `/docker/nginx-dev/` respectively. The various parts of Bron interact (roughly) as described in the following figure.

![Bron Architecture](https://i.imgur.com/I3DCEJg.png)

The backend (`/backend/jodal`) is responsible for scraping documents from the various sources in Bron, which are exposed through a CLI in `/backend/manage.py`. These are run through hourly and daily cron jobs. Some scrapers (currently only `woo.py`) add jobs to a Redis queue, which are then run in a separate worker container, whereas others fetch documents directly within the scraper itself. All extracted documents are stored using [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html). In a separate cron job, recently processed and published documents are sent to [Binoas](https://github.com/openstate/binoas), an external email alert system.

The documents are exposed for via the API using [Flask](https://flask.palletsprojects.com/en/stable/) (`/backend/app`), which is documented through Swagger on [docs.bron.live](https://docs.bron.live) (or `/docs/api.yml`). Some API routes are defined as blueprints in `routes/`, and some are exposed as `flask_restful` resources in `resources.py`. These come together in `__init__.py`. Other than document search, the API also allows for user-specific actions, such as the creation of feeds about specific keywords and/or organisations.

User accounts and authentication are handled using a self-hosted instance of [FusionAuth](https://fusionauth.io/docs/get-started/). The admin panel is accessible through [users.bron.live](https://users.bron.live). FusionAuth stores all data in the `fusionauth` database of the MySQL instance. The `jodal` database stores all app data specific to a given user. Currently, only the `feed` table is actively used, which stores user-created feeds. The API uses [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) as an ORM to interact with the database.

Finally, the web app is the user-facing part of Bron (together with e-mail alerts). It interacts with Bron only through the API. The web app is developed with [SvelteKit](https://kit.svelte.dev) and is server-side rendered. The web app is split into two route groups: the 'site', for the landing and about pages, and the 'app', for the actual interactive pages such as search.

### Deployment

Bron uses [Fabric](https://www.fabfile.org/) to deploy updates. Run `fab deploy` to deploy. Edit `fabfile.py` to change the deployment pipeline.

### Migrations

Bron uses [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for database migrations:
- Create a migration: `docker exec jodal_backend_1 alembic revision -m "create example table"`
- Migrate: `docker exec jodal_backend_1 alembic upgrade head`
- Rollback: `docker exec jodal_backend_1 alembic downgrade -1`

## Contact

Send an email to developers@openstate.eu.