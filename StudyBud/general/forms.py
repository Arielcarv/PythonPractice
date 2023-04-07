from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from general.models import Room, Message


class RoomForm(ModelForm):
    new_topic = forms.CharField(max_length=200, required=False, label="New Topic (Optional)")

    class Meta:
        model = Room
        required_fields = ["topic", "name"]
        fields = ["new_topic", "topic", "name", "description"]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")

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


class UserProfileUpdateForm(UserChangeForm):
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password")

    def clean_password(self):
        """If password is provided, validate it."""
        password = self.cleaned_data.get("password")
        if password:
            password_validation.validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        """Save user model with new data."""
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
