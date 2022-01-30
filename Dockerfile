FROM python:3.9-alpine
RUN mkdir "/digi-crawler"
WORKDIR /digi-crawler
COPY . /digi-crawler
RUN pip install -r requirements.txt
RUN python3 -m main.py



