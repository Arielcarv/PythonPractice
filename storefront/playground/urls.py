from django.urls import path
from playground.views import home, say


urlpatterns = [
    path("", home, name="home"),
    path("hello/", say, name="hello"),
]
