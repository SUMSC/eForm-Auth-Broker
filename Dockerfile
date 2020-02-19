FROM python:3.6-slim

LABEL VERSION="1.1" MAINTAINER="Amber<wzhzzmzzy@gmail.com>"

EXPOSE 8000

ADD broker.py /opt/broker/broker.py

ADD requirements.txt /opt/broker/requirements.txt

RUN pip install -r /opt/broker/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python3", "/opt/broker/broker.py"]