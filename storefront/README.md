# Django tutorial for beginers [Programming with Mosh](https://youtu.be/rHux0gMZ3Eg)


## Commands:
- Install `pip install pipenv`. And create a virtual environment.

```bash
pipenv install django   # Inside the virtual environment.
pipenv shell            # To activate the environment.
django-admin startproject storefront
```

- Run server:
```bash
python manage.py runserver
```

- Run migrations:
```bash
python manage.py migrate
```

- Start a new APP:
```bash
python manage.py startapp <NameOfTheApp>
```

## Docker images
```bash
docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev

docker run -d -p 6379:6379 redis
```

## Celery setup
```bash
celery -A storefront worker --loglevel=info

celery -A storefront beat

celery -A storefront flower
```
## Running with gunicorn
```
gunicorn storefront.wsgi
```
