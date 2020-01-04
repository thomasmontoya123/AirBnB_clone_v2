#!/usr/bin/python3
'''distributes an archive to your web servers'''
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

    archive_name = "versions/web_static_{}.tgz".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))

    if archive.failed:
        return None
    return archive_name


def do_deploy(archive_path):
    '''creates and distributes an archive to your web servers '''
    if not path.exists(archive_path):
        return False

    try:
        full_name = archive_path[9:]
        short_name = archive_path[9:-4]
        put(archive_path, "/tmp/{}".format(full_name))
        run("mkdir -p /data/web_static/releases/{}/".format(short_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(full_name, short_name))
        run("mv /data/web_static/releases/{}/web_static/*\
                            /data/web_static/releases/{}/"
            .format(short_name, short_name))
        run("rm /tmp/{}".format(full_name))
        run("rm -fr /data/web_static/current")
        run("rm -fr /data/web_static/releases/{}/web_static"
            .format(short_name))
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(short_name))
        print("New version deployed!")
    except Exception:
        return False


def deploy():
    '''full deployment'''
    new = do_pack()
    if not new:
        return False
    return do_deploy(new)
