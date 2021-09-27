FROM python:3.8.3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./req.txt /usr/src/app/req.txt
RUN pip install -r req.txt

COPY . /usr/src/app


EXPOSE 8000

