from django.shortcuts import render
from store.models import Product


def home(request):
    all_products = Product.objects.all()
    return render(request, "home.html", {"products": all_products})


def say(request):
    return render(request, "hello.html")
