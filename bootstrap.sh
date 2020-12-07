#!/bin/bash
docker-compose build;
docker-compose up -d;
docker-compose run omcp python3 manage.py migrate;
docker-compose run omcp python3 manage.py seed --mode=refresh;