from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Item


def home(request: HttpRequest) -> HttpResponse:
    context = {"items": Item.objects.all()}
    return render(request, "frontend/home.html", context=context)
