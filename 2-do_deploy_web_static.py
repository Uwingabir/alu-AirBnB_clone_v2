#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['100.27.187.5', '54.167.59.7']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        # Extract file name and remove the extension
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to /tmp/ directory
        put(archive_path, "/tmp/{}".format(file_n))

        # Create the target release directory
        run("mkdir -p {}{}/".format(path, no_ext))

        # Unpack the archive
        run("tar -xzf /tmp/{} -C {}{}/".format(file_n, path, no_ext))

        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}".format(file_n))

        # Move the contents out of the web_static folder
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))

        # Remove the now-empty web_static folder
        run("rm -rf {}{}/web_static".format(path, no_ext))

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new release
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))

        # Ensure proper ownership of the new files
        run('chown -R ubuntu:ubuntu /data/web_static/releases/{}/'.format(no_ext))

        # Return True if everything is successful
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
