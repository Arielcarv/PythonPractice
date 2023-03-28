from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    UpdateView,
)

from common.util import CustomLoginRequiredMixin
from general.forms import RoomForm, SignUpForm, MessageForm
from general.models import Room, Topic, Message


class LoginPage(View):
    template_name = "login.html"
    context = {}

    def get(self, request):
        return render(request, "login.html", self.context)

    # TODO: Implement LoginView
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
        messages = Message.objects.filter(
            Q(room__topic__name__iregex=url_params)
        )
        context = {
            "rooms": rooms,
            "room_count": room_count,
            "topics": topics,
            "room_messages": messages,
        }
        return render(request, "general/home.html", context)


class RoomView(CustomLoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "general/room.html"
    context = {}
    success_message = "Message registered successfully"

    @staticmethod
    def get(request, pk):
        room = Room.objects.get(id=pk)
        messages = room.message_set.all().order_by("-created")
        participants = room.participants.all()
        context = {
            "room": room,
            "room_messages": messages,
            "participants": participants,
        }
        return render(request, "general/room.html", context)

    def form_valid(self, form):
        """This validates the form by adding room and user to it."""
        form.instance.author = self.request.user
        form.instance.room = Room.objects.get(pk=self.kwargs.get("pk"))
        form.instance.room.participants.add(form.instance.author)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("room", kwargs={"pk": self.kwargs.get("pk")})


class UserProfilePage(CustomLoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "general/profile.html"
    context_object_name = "user"

    def get(self, request, pk):
        user = get_object_or_404(self.model, id=pk)
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {
            "user": user,
            "rooms": rooms,
            "room_messages": room_messages,
            "topics": topics,
        }
        return render(request, self.template_name, context)


class CreateRoom(CustomLoginRequiredMixin, FormView):
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class UpdateRoom(UserPassesTestMixin, UpdateView):
    model = Room
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def test_func(self):
        """Check if the user is the host of the room or is a superuser."""
        if (
            self.request.user == self.get_object().host
            or self.request.user.is_superuser
        ):
            return True
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


class DeleteMessage(CustomLoginRequiredMixin, DeleteView):
    model = Message
    template_name = "general/delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Message deleted successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("room", kwargs={"pk": self.object.room_id})
