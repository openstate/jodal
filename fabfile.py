import os.path

from fabric import Connection, Config, task
from invoke import Exit
import getpass

# Name of the git repository
GIT_REPO = 'jodal'

# Path of the directory
DIR = '/home/projects/%s' % (GIT_REPO)

# nginx container
NGINX_CONTAINER = 'jodal_nginx_1'

# App container
APP_CONTAINER = 'jodal_backend_1'

# API container
API_CONTAINER = 'api-jodal'

# Server name
SERVER = 'fluorine'


@task
def deploy(c):
    sudo_pass = getpass.getpass("Enter your sudo password on %s: " % SERVER)
    config = Config(overrides={'sudo': {'password': sudo_pass}})
    c = Connection(SERVER, config=config)

    # Pull from GitHub
    c.run(
        'cd %s && git pull git@github.com:openstate/%s.git' % (
            DIR,
            GIT_REPO
        )
    )

    # build & start new containers
    c.sudo("sh -c 'cd %s && docker-compose build'" % (os.path.join(DIR, 'docker'),))
    c.sudo("sh -c 'cd %s && docker-compose up -d'" % (os.path.join(DIR, 'docker'),))

    # Upgrade database
    c.sudo('docker exec %s alembic upgrade head' % (APP_CONTAINER))

    # put elasticsearch mapings
    c.sudo('docker exec %s python manage.py elasticsearch put_templates' % (APP_CONTAINER))
    # reload api container
    c.sudo("sh -c 'cd %s && docker-compose restart %s'" % (os.path.join(DIR, 'docker'), API_CONTAINER))
    # Reload app
    c.sudo('docker exec %s nginx -s reload' % (NGINX_CONTAINER))
