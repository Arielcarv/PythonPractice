from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from general.models import Room, Message


class RoomForm(ModelForm):
    new_topic = forms.CharField(
        max_length=200, required=False, label="New Topic (Optional)"
    )

    class Meta:
        model = Room
        required_fields = ["topic", "name"]
        fields = ["new_topic", "topic", "name", "description"]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
