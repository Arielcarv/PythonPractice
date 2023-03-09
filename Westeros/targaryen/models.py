from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    birth_year = models.PositiveSmallIntegerField()
