FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app
COPY ./ /app

RUN apk add --no-cache \
    ttf-dejavu \
    ghostscript \
    bash

RUN uv sync

CMD ["sh", "-c", "uv run python3 manage.py migrate && uv run gunicorn root.wsgi:application --bind 0.0.0.0:8001 --workers 13 --timeout 300"]
