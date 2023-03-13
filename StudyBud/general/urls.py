from django.urls import path

from .views import Home, RoomView, CreateRoom

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("room/<str:pk>", RoomView.as_view(), name="room"),
    path("create-room", CreateRoom.as_view(), name="create-room"),
]
