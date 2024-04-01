# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.11.8-alpine3.19 AS builder
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
RUN mkdir -p /app/logs
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
