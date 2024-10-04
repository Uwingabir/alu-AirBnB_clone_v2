#!/usr/bin/python3
"""Fabric script to deploy an archive to web servers."""

from fabric import Connection, task
from os.path import exists
import os

# Define the hosts
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your server IPs
env.user = 'your_username'  # Replace with your SSH username
env.key_filename = '~/.ssh/id_rsa'  # Default path to your SSH private key

@task
def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False

    try:
        file_n = os.path.basename(archive_path)
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the server
        for host in env.hosts:
            conn = Connection(host=host, user=env.user, connect_kwargs={"key_filename": env.key_filename})
            
            # Upload the archive to /tmp/
            conn.put(archive_path, '/tmp/')
            
            # Create the directory to extract the archive
            conn.run('mkdir -p {}{}/'.format(path, no_ext))
            
            # Uncompress the archive to the specified directory
            conn.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
            
            # Delete the archive from the server
            conn.run('rm /tmp/{}'.format(file_n))
            
            # Remove the current symlink
            conn.run('rm -rf /data/web_static/current')
            
            # Create a new symlink to the new version
            conn.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        
        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False

# To execute the task, use:
# fab -H <IP web-01>,<IP web-02> do_deploy:/path/to/archive
