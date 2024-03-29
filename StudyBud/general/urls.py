from django.urls import path

from .views import (
    ActivitiesView,
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
    UserProfileUpdate,
    Topics,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("topics", Topics.as_view(), name="topics"),
    path("activities", ActivitiesView.as_view(), name="activities"),
    path("login", LoginPage.as_view(), name="login"),
    path("logout", LogoutPage.as_view(), name="logout"),
    path("register", RegisterPage.as_view(), name="register"),
    path("profile/<int:pk>", UserProfilePage.as_view(), name="profile"),
    path("profile-update/", UserProfileUpdate.as_view(), name="profile-update"),
    path("room/<int:pk>", RoomView.as_view(), name="room"),
    path("create-room", CreateRoom.as_view(), name="create-room"),
    path("update-room/<int:pk>", UpdateRoom.as_view(), name="update-room"),
    path("delete-room/<int:pk>", DeleteRoom.as_view(), name="delete-room"),
    path(
        "delete-message/<str:pk>",
        DeleteMessage.as_view(),
        name="delete-message",
    ),
]
