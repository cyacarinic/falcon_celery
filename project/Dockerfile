FROM python:3.6.8-alpine
MAINTAINER Claudio Yacarini <cyacarinic@gmail.com>

WORKDIR /usr/local/opt
COPY ./requirements.txt /usr/local/opt/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/local/opt
