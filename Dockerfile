MAINTAINER mohamad
FROM python:3.9

RUN mkdir /digi-crawler
COPY . /digi-crawler
WORKDIR /digi-crawler
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt


