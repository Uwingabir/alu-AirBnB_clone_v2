#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt-get update -y
sudo apt-get install -y nginx

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link, force (-f) remove it if it exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content from the symbolic link
# The alias directive is used to map /hbnb_static to /data/web_static/current/
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
# Restart Nginx to apply changes
sudo service nginx restart

# Ensure script exits successfully
exit 0
