## OMCP (Online Medical Consultation Platform) Service Prototype
### Setup Environment
#### Prerequisites
- 🐳 Docker for Desktop

### Application Configuration
#### 🚜 1st. Build Image
```bash
$ docker-compose build
```
#### 🏎 2nd. Run Application
```bash
$ docker-compose up -d
``` 

#### 🚛 3rd. Database Migration
```bash
$ docker-compose run omcp python manage.py migrate
```