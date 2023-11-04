#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of web_static

# Update and install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow incoming HTTP traffic (port 80) with iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Save the iptables rules to persist across reboots
sudo iptables-save > /etc/iptables.rules

# Install and enable the Uncomplicated Firewall (UFW)
sudo apt-get -y install ufw
sudo ufw allow 'Nginx HTTP'
sudo ufw enable

# Create directory structure
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Change ownership
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve the static content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx
sudo service nginx restart
