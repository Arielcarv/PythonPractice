from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, DeleteView, CreateView

from common.util import CustomLoginRequiredMixin
from general.forms import RoomForm, SignUpForm
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
        except get_user_model().DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect("login")


class RegisterPage(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = "register.html"
    context = {}
    success_url = reverse_lazy("home")
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        """This validates the form and logs in the user"""
        form.instance.username = form.cleaned_data.get("username")
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LogoutPage(LogoutView):
    next_page = reverse_lazy("login")


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


class RoomView(CustomLoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        room = Room.objects.get(id=pk)
        context = {"room": room}
        return render(request, "general/room.html", context)


class CreateRoom(CustomLoginRequiredMixin, FormView):
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.save()
        return super().form_valid(form)


class UpdateRoom(UserPassesTestMixin, UpdateView):
    model = Room
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def test_func(self):
        """Check if the user is the host of the room or is a superuser."""
        print("Inside test_func")
        if (
            self.request.user == self.get_object().host
            or self.request.user.is_superuser
        ):
            return True
        print(self.get_object().host)
        PermissionDenied("You are not the host of this room.")

    def form_valid(self, form):
        """Test if the form sent is valid."""
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to handle the PermissionDenied exception."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(
                self.request, "You don't have permission to access this room."
            )
            return redirect("home")


class DeleteRoom(CustomLoginRequiredMixin, DeleteView):
    model = Room
    template_name = "general/delete.html"
    context_object_name = "room"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Room deleted successfully")
        return super().form_valid(form)
