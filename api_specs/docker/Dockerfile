FROM python:3.11-slim

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade setuptools pip wheel
RUN pip install -r requirements.txt