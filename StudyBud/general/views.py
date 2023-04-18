from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
)

from common.util import CustomLoginRequiredMixin
from general.forms import (
    RoomForm,
    SignUpForm,
    MessageForm,
    UserProfileUpdateForm,
)
from general.models import Room, Topic, Message


class LoginPage(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


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


class Home(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self):
        url_params = self.request.GET.get("query") if self.request.GET.get("query") else ""
        rooms = Room.objects.filter(
            Q(topic__name__endswith=url_params)
            | Q(name__iregex=url_params)
            | Q(description__iregex=url_params)
        )
        topics = Topic.objects.all()[0:5]
        room_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__iregex=url_params))
        context = {
            "rooms": rooms,
            "room_count": room_count,
            "topics": topics,
            "room_messages": room_messages,
        }
        return context


class Topics(TemplateView):
    template_name = "general/topics.html"

    def get_context_data(self):
        url_params = self.request.GET.get("query") if self.request.GET.get("query") else ""
        topics = Topic.objects.filter(Q(name__endswith=url_params))
        context = {"topics": topics}
        return context


class ActivitiesView(TemplateView):
    template_name = "general/activities.html"

    def get_context_data(self):
        room_messages = Message.objects.all().order_by("-created")
        context = {
            "room_messages": room_messages,
        }
        return context


class RoomView(CustomLoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "general/room.html"
    context = {}
    success_message = "Message registered successfully"

    def get_context_data(self):
        room = Room.objects.get(id=self.kwargs.get("pk"))
        room_messages = room.message_set.all().order_by("-created")
        participants = room.participants.all()
        context = {
            "room": room,
            "room_messages": room_messages,
            "participants": participants,
        }
        return context

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

    def get_context_data(self, **kwargs):
        user = self.get_object()
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {
            "user": user,
            "rooms": rooms,
            "room_messages": room_messages,
            "topics": topics,
        }
        return context


class UserProfileUpdate(CustomLoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateForm
    template_name = "general/profile-update.html"
    context_object_name = "user"

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        password = form.cleaned_data.get("password")
        form.instance.set_password(password) if password else setattr(
            form.instance,
            "password",
            get_user_model().objects.only("password").get().password,
        )
        return super().form_valid(form)


class CreateRoom(CustomLoginRequiredMixin, CreateView):
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if "new_topic" in form.changed_data:
            topic = Topic.objects.create(name=form.cleaned_data.get("new_topic"))
            form.instance.topic = topic
        form.instance.host = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        return context


class UpdateRoom(UserPassesTestMixin, UpdateView):
    model = Room
    template_name = "general/room_form.html"
    form_class = RoomForm
    success_url = reverse_lazy("home")

    def test_func(self):
        """Check if the user is the host of the room or is a superuser."""
        if self.request.user == self.get_object().host or self.request.user.is_superuser:
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
            messages.error(self.request, "You don't have permission to access this room.")
            return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        return context


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
