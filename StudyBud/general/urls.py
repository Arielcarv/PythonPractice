from django.urls import path

from .views import (
    CreateRoom,
    DeleteMessage,
    DeleteRoom,
    Home,
    LoginPage,
    LogoutPage,
    UserProfilePage,
    RegisterPage,
    RoomView,
    UpdateRoom,
)

urlpatterns = [
    path("login", LoginPage.as_view(), name="login"),
    path("register", RegisterPage.as_view(), name="register"),
    path("profile/<str:pk>", UserProfilePage.as_view(), name="profile"),
    path("logout", LogoutPage.as_view(), name="logout"),
    path("", Home.as_view(), name="home"),
    path("room/<str:pk>", RoomView.as_view(), name="room"),
    path("create-room", CreateRoom.as_view(), name="create-room"),
    path("update-room/<str:pk>", UpdateRoom.as_view(), name="update-room"),
    path("delete-room/<str:pk>", DeleteRoom.as_view(), name="delete-room"),
    path(
        "delete-message/<str:pk>",
        DeleteMessage.as_view(),
        name="delete-message",
    ),
    # path("topic/<str:pk>", DeleteRoom.as_view(), name="topic"),
]
