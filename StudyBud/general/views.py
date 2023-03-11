from django.shortcuts import render

from general.models import Room


def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "general/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "general/room.html", context)
