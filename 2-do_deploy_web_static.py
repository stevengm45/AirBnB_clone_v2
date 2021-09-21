#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static """
from fabric.api import local, put, run, env
from os import path
from datetime import datetime

env.hosts = ['{}@35.237.172.23'.format(env.user), '{}@34.75.60.230'.format(
    env.user)]


def do_pack():
    """ Create directory if doesn't exist and backup folder web_static """
    time = str(datetime.now()).split(".")[0].replace(
        ":", "").replace(" ", "").replace("-", "")
    if path.exists("versions"):
        local("tar -czf versions/web_static_{}.tgz web_static".format(time))
    else:
        local("mkdir -p versions")
        local("tar -czf versions/web_static_{}.tgz web_static".format(time))


def do_deploy(archive_path):
    """ Deploy a new file to web_static """
    if not path.exists(archive_path):
        return False

    try:
        # Put the file in /tmp/ directory
        put(archive_path, "/tmp/")

        # File token and variables to be used
        tgz = archive_path.split("/")[-1]
        folder = "/data/web_static/releases/{}/".format(tgz[:-4])
        tmp_directory = "/tmp/{}".format(tgz)
        symlink = "/data/web_static/current"

        # Create the folder to uncompress targz
        run("mkdir -p {}".format(folder))

        # Uncompress the tgz file
        run("tar -xzf {} -C {}".format(tmp_directory, folder))

        # Delete the tgz files
        run("rm {}".format(tmp_directory))

        # Move the folder web_static from tgz
        run("mv {}web_static/* {}".format(folder, folder))

        # rm web_static
        run("rm -rf {}web_static".format(folder))

        # Delete the symbolic link
        run("rm -rf {}".format(symlink))

        # Create a new symbolic link
        run("ln -s {} {}".format(folder, symlink))
        return True
    except:
        return False
