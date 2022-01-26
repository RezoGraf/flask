# HELIOS
========================
## Сессии
-------------------------

Забрать переменную из сессии:

    from flask import session
    if 'var' in session:
        var  = session.get('var')
    else:
        pass

Задать переменную в сессию:

    session['var'] = var

Удалить переменную в сессии:

    session.pop('var', None)

Удалить сессию:

    session.clear()

В данном случае под сессией буде подразумеваться cookie который записывается в браузер профиля активного пользователя. Но есть возможность хранить сессию в бд вроде redis дя активных пользователей.

---
##  Запуск в докер контейнере
-------------------------

Запуск uWSGI:

    $ uwsgi --socket 0.0.0.0:7000 --protocol=http -w wsgi:app


Dockerfile:

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

Создание docker файла и запуск:

    $ docker build -t helios .
    $ docker run -d --restart=always -p 9000:9000 -p 9001:9001 helios
