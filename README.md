## OMCP (Online Medical Consaltation Platform) Service Prototype
### Setup Environment
#### Prerequisites
- Docker for Desktop

### Application Configuration
#### 1st. Init Project
```bash
$ docker-compose run omcp django-admin startproject omcp .
```
#### 2nd. Run Application
```bash
$ docker-compose up -d
``` 

#### 3rd. Applied Database Schema With Django ORMS
```bash
$ docker-compose run omcp python manage.py migrate
```