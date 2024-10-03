#!/usr/bin/python3
"""Fabric Script that distributes an archive."""

from fabric import Connection, task
from os.path import exists

# Define the hosts
env_hosts = ['100.27.187.5', '54.167.59.7']

@task
def do_deploy(c, archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the server
        c.put(archive_path, '/tmp/')
        
        # Create the target directory
        c.run('mkdir -p {}{}/'.format(path, no_ext))
        
        # Extract the archive
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        
        # Clean up the temporary file
        c.run('rm /tmp/{}'.format(file_n))
        
        # Move the contents of web_static to the new release folder
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        
        # Remove the now-empty web_static directory
        c.run('rm -rf {}{}/web_static'.format(path, no_ext))
        
        # Remove the current symlink
        c.run('rm -rf /data/web_static/current')
        
        # Create a new symlink to the new version
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        
        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False

# To execute the task, use:
# fab -H <host_ip> do_deploy:/path/to/archive
