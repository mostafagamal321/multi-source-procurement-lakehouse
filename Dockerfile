FROM python:3.11-slim-bookworm

WORKDIR /opt/app

ENV PYTHONPATH=/opt/app \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .