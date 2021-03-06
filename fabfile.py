
from fabric.api import local, run, cd, settings, sudo, env, put
import os

# http://stackoverflow.com/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user
# FIXME: These should be env. variables.
PROJECT_DIR   = "/home/ubuntu/work/gisted"
NVM_DIR       = "/home/ubuntu/.nvm"
VENV_ACTIVATE = os.path.join(PROJECT_DIR, "bin/activate")

env.use_ssh_config = True

def virtualenv(command):
    run(". " + VENV_ACTIVATE + ' && ' + command)

# Invokable commands:

def init_app():
    # Should run 'git clone' here.
    with cd(PROJECT_DIR):
        run("virtualenv --distribute venv")

def update():
    with cd(PROJECT_DIR):
        run("git pull origin master")
        run("export NVM_DIR={dir}".format(dir=NVM_DIR))
        virtualenv("pip install -r requirements.txt")
        #virtualenv("npm install")
        #virtualenv("bower install")
        put("confs/api.conf", "confs/api.conf")
        put("confs/server.key", "confs/server.key")
        put("confs/gisted_in.crt", "confs/gisted_in.crt")
        run("make clean all")

def reload_daemons():
    with cd(PROJECT_DIR):
        with settings(warn_only=True):
            sudo("stop gunicorn-gisted")
            sudo("/etc/init.d/nginx stop")
        sudo("cp confs/gunicorn-upstart.conf /etc/init/gunicorn-gisted.conf")
        sudo("cp confs/nginx.conf /etc/nginx/sites-enabled/gisted.conf")
        sudo("cp confs/logrotate.conf /etc/logrotate.d/gunicorn-gisted")
        sudo("start --verbose gunicorn-gisted")
        sudo("/etc/init.d/nginx start")

def deploy():
    update()
    reload_daemons()
