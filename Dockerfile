FROM python:3.7-slim

LABEL maintainer="OpenStax Content Engineering"

RUN apt-get update
RUN apt-get install -y build-essential

ENV CODE_DIR=/code/scripts
COPY ./requirements.txt /code/scripts/
WORKDIR /code/scripts

RUN pip install -r requirements.txt

COPY ./*.py ./sync.sh /code/scripts/

ENTRYPOINT ["./sync.sh"]
