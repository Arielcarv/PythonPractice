from django.urls import path

from .views import Home, RoomView, CreateRoom, UpdateRoom, DeleteRoom, LoginPage

urlpatterns = [
    path("login", LoginPage.as_view(), name="login"),
    path("", Home.as_view(), name="home"),
    path("room/<str:pk>", RoomView.as_view(), name="room"),
    path("create-room", CreateRoom.as_view(), name="create-room"),
    path("update-room/<str:pk>", UpdateRoom.as_view(), name="update-room"),
    path("delete-room/<str:pk>", DeleteRoom.as_view(), name="delete-room"),
    # path("topic/<str:pk>", DeleteRoom.as_view(), name="topic"),
]
