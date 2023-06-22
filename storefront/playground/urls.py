from django.urls import path
from playground.views import email_sender, home, say


urlpatterns = [
    path("", home, name="home"),
    path("hello/", say, name="hello"),
    path("send/", email_sender, name="send"),
]
