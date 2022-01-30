# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /digi-crawler
COPY . /digi-crawler
RUN pip install -r requirements.txt
RUN python3 -m
