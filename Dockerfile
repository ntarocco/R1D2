FROM python:3.6

MAINTAINER Nicola Tarocco "nicola.tarocco@cern.ch"

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENV R1D2_LOGGING_LEVEL INFO

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", ":8000", "--timeout", "120", "--graceful-timeout", "60", "app:app"]
