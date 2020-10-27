FROM python:3.6.6

WORKDIR /

RUN pip3 install --upgrade pip \
&& pip3 install ccxt=1.22.16 numpy pandas redis stockstats schedule pymysql pyCryptodome matplotlib flask sqlalchemy uwsgi websocket websocket-client

