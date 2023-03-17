from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, UpdateView, DeleteView

from common.util import CustomLoginRequiredMixin
from general.forms import RoomForm
from general.models import Room, Topic


class LoginPage(View):
    template_name = "login.html"
    context = {}

    def get(self, request):
        return render(request, "login.html", self.context)

    @staticmethod
    def post(request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        try:
            get_user_model().objects.get(username=username)
            login(request, user)
            return redirect("home")
        except AttributeError:
            messages.error(request, "Invalid username or password.")
            return redirect("login")


class LogoutPage(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("login")


class Home(View):
    @staticmethod
    def get(request):
        url_params = (
            request.GET.get("query") if request.GET.get("query") else ""
        )
        rooms = Room.objects.filter(
            Q(topic__name__iregex=url_params)
            | Q(name__iregex=url_params)
            | Q(description__iregex=url_params)
        )
        topics = Topic.objects.all()
        room_count = rooms.count()
        context = {"rooms": rooms, "room_count": room_count, "topics": topics}
        return render(request, "general/home.html", context)


class RoomView(View):
    @staticmethod
    def get(request, pk):
        room = Room.objects.get(id=pk)
        context = {"room": room}
        return render(request, "general/room.html", context)


class CreateRoom(CustomLoginRequiredMixin, FormView):
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.save()
        return super().form_valid(form)


class UpdateRoom(UserPassesTestMixin, UpdateView):
    model = Room
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = "/"

    def test_func(self):
        print("Inside test_func")
        if self.request.user == self.get_object().host:
            return True
        print(self.get_object().host)
        PermissionDenied("You are not the host of this room.")

    def form_valid(self, form):
        return super().form_valid(form)

    # TODO: Fix this dispatch method calmly, and put error treatment in the template
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            error_message = "You don't have permission to access this page."
            # return render(request, "general/home.html", {"error_message": error_message}, status=200)
            return redirect("home")


class DeleteRoom(CustomLoginRequiredMixin, DeleteView):
    model = Room
    template_name = "general/delete.html"
    context_object_name = "room"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Room deleted successfully")
        return super().form_valid(form)
