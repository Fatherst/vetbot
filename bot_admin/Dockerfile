FROM python:3.9.6

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install pipenv

WORKDIR /usr/src/bot_admin

COPY . /usr/src/bot_admin

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .