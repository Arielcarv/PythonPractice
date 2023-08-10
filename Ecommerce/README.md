## E-commerce app with Django from Udemy

## Commands:
- Create a virtual environment.
```bash
python -m venv <name-of-virtualenv>
python -m venv venv
source venv/bin/activate    # Activate virtual environment
pip install -r requirements # Inside the virtual environment.
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
- To access the Objects from database. First you need to access project shell.
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
