from django.urls import path
from api.views import GetRoutes, GetRooms, GetRoom

urlpatterns = [
    path("", GetRoutes.as_view(), name="api_base"),
    path("rooms/", GetRooms.as_view(), name="all_rooms"),
    path("room/<int:pk>", GetRoom.as_view(), name="get_room"),
]
