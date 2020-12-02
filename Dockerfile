#base image
FROM python:3

ENV PYTHONBUFFERED 1

#directory to store app source code
RUN mkdir /omcp

#switch to /app directory so that everything runs from here
WORKDIR /omcp

#copy the app code to image working directory
COPY ./omcp /omcp

#let pip install required packages
RUN pip install -r requirements.txt
