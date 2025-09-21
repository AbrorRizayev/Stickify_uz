FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app
COPY ./ /app
RUN apk add --no-cache \
    ttf-dejavu \
    ghostscript \
    bash

RUN uv sync

CMD ["uv","run","python3", "manage.py", "runserver", "0:8001"]