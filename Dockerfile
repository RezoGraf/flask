FROM ubuntu:latest
MAINTAINER Helios 'helios@oksp42.ru'
RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.10 python3-pip libldap2-dev python-dev build-essential libsasl2-dev libssl-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./helios
WORKDIR /helios
CMD ["uwsgi", "--http", "0.0.0.0:9000", "--wsgi-file", "/helios/wsgi.py", \
    "--callable", "app", "--stats", "0.0.0.0:9001"]
