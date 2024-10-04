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


# Modify Nginx configuration to support multiple hosts
# server_name directive will listen for localhost, 100.27.187.5, and 54.167.59.7
sudo sed -i '/server_name _;/c\\tserver_name localhost 100.27.187.5 54.167.59.7;' /etc/nginx/sites-available/default

# Add the location block to serve /hbnb_static from /data/web_static/current/
sudo sed -i '/server_name localhost/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

# Ensure script exits successfully
exit 0
