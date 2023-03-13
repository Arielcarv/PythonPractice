from django.shortcuts import render, redirect
from django.views.generic import View

from general.forms import RoomForm
from general.models import Room


class Home(View):
    @staticmethod
    def get(request):
        rooms = Room.objects.all()
        context = {"rooms": rooms}
        return render(request, "general/home.html", context)


class RoomView(View):
    @staticmethod
    def get(request, pk):
        room = Room.objects.get(id=pk)
        context = {"room": room}
        return render(request, "general/room.html", context)


class CreateRoom(View):
    @staticmethod
    def get(request):
        form = RoomForm()
        context = {"form": form}
        return render(request, "general/room_form.html", context)

    @staticmethod
    def post(self, request):
        name = request.POST["name"]
        description = request.POST["description"]
        room = Room(name=name, description=description)
        room.save()
        return redirect("home")
