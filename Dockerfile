FROM python:3.6.6

WORKDIR /

RUN pip3 install --upgrade pip \
&& pip3 install ccxt numpy pandas redis stockstats schedule pymysql pyCryptodome matplotlib flask sqlalchemy uwsgi websocket websocket-client

