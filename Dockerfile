FROM orchardup/python:2.7
RUN apt-get update -qq 

RUN mkdir /code
ADD . /code/

WORKDIR /code/
RUN pip install -r requirements.txt

WORKDIR /code/drf-api-test

EXPOSE 8080
