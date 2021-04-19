import sys
import os

NGINX_CONFIG_DIRECTORY = '/etc/nginx/sites-enabled/'

TEMPLATE = '''server {
    server_name <<SERVER_NAME>>;
    return 301 https://<<SERVER_NAME>>$request_uri;
}

# HTTPS - proxy all requests to the Node app
server {
    # Enable HTTP/2
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name <<SERVER_NAME>>;

    # Use the Lets Encrypt certificates
    ssl_certificate /etc/letsencrypt/live/<<SERVER_NAME>>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<<SERVER_NAME>>/privkey.pem;

    # Include the SSL configuration from cipherli.st
    include snippets/ssl-params.conf;

    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://localhost:<<SERVER_PORT>>/;
        proxy_ssl_session_reuse off;
        proxy_set_header Host $http_host;
        proxy_cache_bypass $http_upgrade;
        proxy_redirect off;
    }
}
'''

SERVER_NAME = input('Enter Server Name (example.website.com): ')
SERVER_PORT = input('Enter Server Port: ') 

CONFIG_TEXT = TEMPLATE.replace('<<SERVER_NAME>>', SERVER_NAME).replace('<<SERVER_PORT>>', SERVER_PORT)

if not os.path.exists(NGINX_CONFIG_DIRECTORY):
    os.makedirs(NGINX_CONFIG_DIRECTORY)

with open(NGINX_CONFIG_DIRECTORY + SERVER_NAME, 'w') as f:
    f.write(CONFIG_TEXT)