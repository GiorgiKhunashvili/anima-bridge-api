#pull official base image
FROM python:3.7.2

#set work dir
WORKDIR /usr/src/app

#set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#install dependencies
RUN pip install --upgrade pip
COPY  ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY ./ /usr/src/app/
