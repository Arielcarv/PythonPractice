# Django tutorial for begginers [Programming with Mosh](https://youtu.be/rHux0gMZ3Eg)

Link for the [Official Django tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)

## Commands:
- Install `pip install pipenv`. And create a virtual environment.

```bash
pipenv install django   # Inside the virtual environment.
pipenv shell            # To activate the environment.
django-admin startproject front
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
## Shell commands to query database:
- On this example we are going to access the Question and Choice Object from database. First you need to access project shell.
```bash
python manage.py shell
```
- Then interact with objects through ORM (Object Relational Mapper)
```python
>> from polls.models import Choice, Question
>> Question.Objects.all() # Show all Questions objects.
>> Question.Objects.get(pk=<number>) # pk=Primary key.
>> Question._meta.get_fields() # Show all Question fields with details.
>> Choice.Objects.all() # Show all Choice objects.
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
