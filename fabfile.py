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

# Container used to compile the assets
NODE_CONTAINER = 'jodal_node_1'

# App container
APP_CONTAINER = 'jodal_backend_1'
# makesite container
MAKESITE_CONTAINER = 'jodal_makesite_1'

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

    # compile web landing page
    c.sudo("docker exec %s ./makesite.py" % (MAKESITE_CONTAINER,))
    # Compile assets
    output = c.sudo(
        'docker inspect --format="{{.State.Status}}" %s' % (NODE_CONTAINER)
    )
    if output.stdout.strip() != 'running':
        raise Exit(
            '\n*** ERROR: The %s container, used to compile the assets, is '
            'not running. Please build/run/start the container.' % (
                NODE_CONTAINER
            )
        )
    c.sudo('docker exec %s yarn' % (NODE_CONTAINER))
    c.sudo('docker exec %s yarn build' % (NODE_CONTAINER))

    # Upgrade database
    c.sudo('docker exec %s alembic upgrade head' % (APP_CONTAINER))

    # put elasticsearch mapings
    c.sudo('docker exec %s python manage.py elasticsearch put_templates' % (APP_CONTAINER))
    # Reload app
    c.sudo('docker exec %s nginx -s reload' % (NGINX_CONTAINER)) 
