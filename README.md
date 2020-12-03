## OMCP (Online Medical Consultation Platform) Service Prototype
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

#### 3rd. Database Migration
```bash
$ docker-compose run omcp python manage.py migrate
```