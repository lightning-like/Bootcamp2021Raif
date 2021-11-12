# Docker file for the base image with cuda support, installed postgres and python libs
# Run outside of Raiff VPN
# tag: artifactory.raiffeisen.ru/alternative_data-docker/base_image:py38

FROM python:3.7.4
RUN apt-get update ; apt-get install -yqq \
        python3-pip \
        nano curl iputils-ping telnet vim wget \
        git \

ADD . /app
ENV PYTHONPATH='/app'

ADD ./requirements.txt /requirements.txt
RUN pip3 install

