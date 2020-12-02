#!/bin/bash
docker-compose run omcp python3 manage.py migrate;
docker-compose run omcp python3 manage.py createsuperuser;