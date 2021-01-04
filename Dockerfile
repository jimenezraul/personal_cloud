FROM python:3

ENV PYTHONONBUFFERED 1

WORKDIR /app

RUN mkdir /app/media

RUN mkdir /app/media/cloud

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app


