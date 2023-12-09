import random
import string
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Room

# Create your views here.

class CreateRommView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            room_id = generate_room_id()
            room = Room(room_id = room_id, lecture = user)
            room.save()
            return Response(data=room_id, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)






def generate_room_id(length=8):
    characters = string.ascii_letters + string.digits
    room_id = ''.join(random.choice(characters) for i in range(length))
    return room_id
