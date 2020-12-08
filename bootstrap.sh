#!/bin/bash
docker-compose build;
docker-compose up -d db;
docker-compose up -d omcp;
docker-compose run omcp python3 manage.py migrate;
docker-compose run omcp python3 manage.py seed --mode=refresh;