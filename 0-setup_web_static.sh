#!/usr/bin/env bash
# Install Nginx if not already installed

sudo useradd ubuntu

if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories and files
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_content=$(cat <<EOF
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
    }

    location / {
        add_header X-Served-By $HOSTNAME;
        proxy_set_header Host $HOSTNAME;
        proxy_pass http://127.0.0.1:5000;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }
}
EOF
)
echo "$config_content" | sudo tee "$config_file"

# Restart Nginx
sudo service nginx restart
