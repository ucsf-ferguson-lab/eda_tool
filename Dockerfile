FROM python:3.14.0-slim

RUN apt-get update && apt-get install -y \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install -r ./requirements.txt