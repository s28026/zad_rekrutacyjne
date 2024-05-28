FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install fastapi uvicorn redis celery sqlalchemy aiosqlite

WORKDIR /app
