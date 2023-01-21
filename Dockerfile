# pull official base image
FROM python:3.8

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
ADD . /app
COPY ./requirements.txt ./app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app
