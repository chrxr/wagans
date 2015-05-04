from fabric.api import *
import uuid


env.roledefs = {
    'production': ['chris@178.62.92.190']
}

@roles('production')
def deploy(gitonly=False):
    with cd('/home/chris/wagans'):
        run("git pull")
        run("/home/chris/Env/wag2/bin/pip install -r requirements.txt")
        sudo("service nginx restart")
        sudo("service uwsgi restart")

@roles('production')
def get_test():
    get("/home/chris/wagans/test.txt", "/wagans/test.txt", use_sudo=True)

@roles('production')
def fetch_live_data():
    filename = "wagans_%s.sql" % uuid.uuid4()
    local_path = "~/wagans/tmp/%s" % filename
    remote_path = "/tmp/%s" % filename

    run('pg_dump -Upostgres -cf %s wagans' % remote_path)
    run('gzip %s' % remote_path)
    get("%s.gz" % remote_path, "%s.gz" % local_path)
    run('rm %s.gz' % remote_path)
    local('dropdb -Upostgres wagans')
    local('createdb -Upostgres wagans')
    local('gunzip %s.gz' % local_path)
    local('psql -Upostgres wagans -f %s' % local_path)
    local('rm %s' % local_path)


def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    sudo("aptitude update")
    sudo("aptitude -y upgrade")

def install_memcached():
    """ Download and install memcached. """
    sudo("aptitude install -y memcached")

def update_install():

    # Update
    update_upgrade()

    # Install
    install_memcached()