#!/usr/bin/python3
'''Compress before sending '''
from fabric.operations import local
from datetime import datetime


def do_pack():
    '''Compressor function '''
    local("mkdir -p versions")
    archive = local("tar -zcvf versions/web_static_{}.tgz web_static".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))

    if archive.failed:
        return None
    return archive
