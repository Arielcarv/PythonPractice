from django.shortcuts import render
from store.models import Product, OrderItem


def home(request):
    distinct_order_items = OrderItem.objects.values("product_id").distinct()
    products = Product.objects.filter(id__in=distinct_order_items).order_by("title")
    return render(request, "home.html", {"products": list(products)})


def say(request):
    return render(request, "hello.html")
