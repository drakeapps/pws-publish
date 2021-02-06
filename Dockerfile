FROM python:3

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /code/
COPY WundergroundPublish /code/WundergroundPublish
COPY main.py /code/

ENV API_KEY "" \
	STATION_ID ""

ENTRYPOINT [ "python", "-u", "main.py" ]