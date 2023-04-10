from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from general.models import Room
from api.serializers import RoomSerializer


class GetRoutes(APIView):
    def get(self, request):
        routes = [
            "GET /api/ - API",
            "GET /api/rooms/ - get all rooms",
            "GET /api/rooms/:id - get sepcific room",
        ]
        return Response({"routes": routes}, status=status.HTTP_200_OK)


class GetRooms(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True)
        return Response(serialized_rooms.data, status=status.HTTP_200_OK)


class GetRoom(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        room = self.get_object(pk)
        serialized_room = RoomSerializer(room)
        return Response(serialized_room.data, status=status.HTTP_200_OK)
