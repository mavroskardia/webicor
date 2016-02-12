#!/bin/bash

cd /srv/webicor/webicor

gunicorn -b unix:///srv/webicor.sock webicor.wsgi:application &
/usr/bin/nginx -c /etc/nginx/nginx.conf

