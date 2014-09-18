FROM orchardup/python:2.7
RUN apt-get update -qq 

RUN mkdir /code
ADD . /code/

WORKDIR /code/
RUN pip install -r requirements.txt
RUN python setup.py install
RUN python setup.py develop 
WORKDIR /code/test/testproj

