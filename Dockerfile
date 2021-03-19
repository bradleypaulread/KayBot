FROM ubuntu:focal

WORKDIR /bot

COPY . /bot

# do not pause for user input
# https://askubuntu.com/questions/909277/avoiding-user-interaction-with-tzdata-when-installing-certbot->
ARG DEBIAN_FRONTEND=noninteractive

RUN : \
    && apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install ffmpeg \
    && apt-get -y install python3-pip \
    && pip3 install virtualenv

RUN : \
    && virtualenv venv \
    && . venv/bin/activate \
    && pip install -r requirements.txt
