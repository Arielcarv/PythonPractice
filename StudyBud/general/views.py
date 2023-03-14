from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, UpdateView, DeleteView

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


class CreateRoom(FormView):
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.save()
        return super().form_valid(form)


class UpdateRoom(UpdateView):
    model = Room
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteRoom(DeleteView):
    model = Room
    template_name = "general/delete.html"
    context_object_name = "room"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Room deleted successfully")
        return super().form_valid(form)
