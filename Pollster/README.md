# Django Crash Course from [Taversy Media](https://youtu.be/e1IyzVyrLSU)

Link for the [Official Django tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)

### Commands:
- Install `pip install pipenv`. And create a virtual environment.

```bash
pipenv shell
pipenv install django  # Inside the virtual environment.
django-admin startproject pollster
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
### Shell commands to query database:
- On this example we are going to access the Question and Choice Object from database. First you need to access project shell.
```bash
python manage.py shell
```
- Then interact with objects.
```python
>> from polls.models import Choice, Question
>> Question.Objects.all() # Show all Questions objects.
>> Question.Objects.get(pk=<number>) # pk=Primary key.
>> Question._meta.get_fields() # Show all Question fields with details.
>> Choice.Objects.all() # Show all Choice objects.
```


