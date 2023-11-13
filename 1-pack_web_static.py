#!/usr/bin/python3
# Generates a .tgz archive from the contents of web_static.
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    f_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                           dt.month,
                                                           dt.day,
                                                           dt.hour,
                                                           dt.minute,
                                                           dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(f_name)).failed is True:
        return None
    return f_name
