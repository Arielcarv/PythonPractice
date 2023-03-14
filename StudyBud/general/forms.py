from django.forms import ModelForm

from general.models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["topic", "name", "description"]
