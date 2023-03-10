from django.shortcuts import render


def home(request):
    return render(request, "general/home.html")


def room(request):
    return render(request, "general/room.html")
