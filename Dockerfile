FROM pypy:3.6-slim

LABEL VERSION="1.0" MAINTAINER="LionTao <taojiachun31@foxmail.com>"

ADD broker.py /opt/broker/broker.py

ADD requirements.txt /opt/broker/requirements.txt

RUN pip install -r /opt/broker/requirements.txt

EXPOSE 8000

ENTRYPOINT ["pypy3","/opt/broker/broker.py"]