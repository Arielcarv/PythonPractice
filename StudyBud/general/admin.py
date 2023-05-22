from django.contrib import admin

from general.models import Room, Topic, Message, User

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(User)
