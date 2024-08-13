# base image
FROM python:3.12
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create root directory for our project in the container
WORKDIR /server
ADD . .
# install dependencies
RUN pip install --upgrade pip

# run this command to install all dependencies
RUN pip install -r requirements.txt

# port where the Django app runs
# EXPOSE 8000