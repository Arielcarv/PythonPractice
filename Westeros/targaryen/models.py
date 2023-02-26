from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    birth_year = models.PositiveSmallIntegerField()
