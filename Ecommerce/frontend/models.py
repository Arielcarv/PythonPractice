from django.db import models


class Item(models.Model):
    CATEGORY_CHOICES = (("C", "Computer"), ("M", "Mobile"), ("T", "Tablet"))

    LABEL_CHOICES = (
        ("N", "New"),
        ("R", "Refurbished"),
        ("U", "Used"),
    )

    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    label = models.CharField(choices=LABEL_CHOICES, max_length=5)
    slug = models.SlugField()
    decription = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title
