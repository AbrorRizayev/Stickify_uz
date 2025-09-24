

server {
    listen 8000;
    server_name online_pdp.fil.uz;

    location /static/ {
        alias /var/www/Stickify.uz/static/;
        expires 30d; # Cache static files for 30 days
    }

    location /media/ {
        alias /var/www/Stickify.uz/media/;
        expires 30d; # Cache media files for 30 days
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Stickify.uz/Stickify.sock;
    }
}