from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from general.models import Room, Topic, Message, User

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(User, UserAdmin)
