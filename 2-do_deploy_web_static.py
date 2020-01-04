#!/usr/bin/python3
'''Distributes an archive to the web servers,
using the function do_deploy'''
from datetime import datetime
from fabric.operations import local, put, run
from fabric.api import env
from os import path

env.hosts = ['35.190.151.31', '35.185.1.2']


def do_pack():
    '''Compressor function '''
    local("mkdir -p versions")
    archive = local("tar -zcvf versions/web_static_{}.tgz web_static".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))

    if archive.failed:
        return None
    return archive


def do_deploy(archive_path):
    """ DEploys """
    if not path.exists(archive_path):
        return False

    full_name = archive_path[9:]
    short_name = archive_path[9:-4]

    try:
        put(archive_path, "/tmp/{}".format(full_name))
        run("mkdir -p /data/web_static/releases/{}".format(short_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(full_name, short_name))
        run("rm /tmp/{}".format(full_name))
        run("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(short_name, short_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(short_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(short_name))
        print("New version deployed!")

    except Exception:
        return False
