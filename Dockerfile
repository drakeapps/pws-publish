FROM python:3-buster

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /code/
COPY WundergroundPublish /code/WundergroundPublish
COPY main.py /code/

ENV API_KEY "" \
	STATION_ID ""

ENTRYPOINT [ "python", "-u", "main.py" ]