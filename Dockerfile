FROM python:3.10
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y cron

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y cron postgresql-client
COPY wait-for-postgres.sh /usr/src/app/wait-for-postgres.sh
RUN chmod +x /usr/src/app/wait-for-postgres.sh


COPY . .