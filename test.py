

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

}


server {
    listen 80;
    server_name your_domain.com www.your_domain.com; # Replace with your domain

    # Serve static files
    location /static/ {
        alias /path/to/your/django_project/static_root/; # Replace with your STATIC_ROOT path
        expires 30d;
    }

    # Serve media files (if applicable)
    location /media/ {
        alias /path/to/your/django_project/media_root/; # Replace with your MEDIA_ROOT path
        expires 30d;
    }

    # Proxy requests to Gunicorn or uWSGI
    location / {
        proxy_pass http://unix:/run/gunicorn.sock; # Or http://127.0.0.1:8000; if using TCP port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_log /var/log/nginx/your_project_error.log;
    access_log /var/log/nginx/your_project_access.log;
}