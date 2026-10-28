FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=mysite.settings.prod

WORKDIR /app

# Existing pinned dependencies include Pillow, lxml, libsass, and PostgreSQL drivers.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

# Static/media files are collected on startup and served by the reverse proxy.
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
