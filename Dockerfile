FROM ubuntu:latest
MAINTAINER Andrey Maksimov 'maksimov.andrei@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /
WORKDIR / 
RUN pip install -r requirements.txt
ENTRYPOINT ['uwsgi']
CMD ['--socket 0.0.0.0:9000 --protocol=http -w wsgi:app']