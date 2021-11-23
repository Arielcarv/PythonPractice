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

