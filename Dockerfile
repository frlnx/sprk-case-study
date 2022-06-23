FROM python:3.9-slim-buster as base

# install psql
RUN apt-get update
RUN apt-get -y install postgresql-client


COPY ./requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN ["pip3", "install", "--no-cache-dir", "-U", "-r", "requirements.txt"]
COPY . /opt/app

# make wait-for-postgres.sh executable
RUN chmod +x wait-for-postgres.sh

ENV PYTHONPATH "${PYTHONPATH}:/opt/app"
