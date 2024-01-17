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
            premium =  user.premium
            room_id = generate_room_id()
            room = Room(room_id = room_id, lecture = user, premium = premium)
            room.save()
            return Response(data=room_id, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get('room_id')
        print(room_id)
        try:
            room = Room.objects.get(room_id = room_id)
            
            if room.premium:
                room.num_of_peer += 1
                room.save()
                return Response(status=status.HTTP_200_OK)
            
            if room.num_of_peer >= 50:
                return Response('Total limit exceeded',status=status.HTTP_406_NOT_ACCEPTABLE)
            
            room.num_of_peer += 1
            room.save()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)





def generate_room_id(length=8):
    characters = string.ascii_letters + string.digits
    room_id = ''.join(random.choice(characters) for i in range(length))
    return room_id
