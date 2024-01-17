from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Thread,ChatMessage
from .serializers import ThreadSerializer,MesageSerializer
from authentication.models import User
from authentication.serializers import UserSerializer

# Create your views here.

class GetAllPeerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            threads = Thread.objects.by_user(user=request.user).order_by('-timestamp')
            serializer = ThreadSerializer(threads,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class GetAllMessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            peerID = request.data.get('userId')
            Tid = request.data.get('Tid')
            thread = Thread.objects.get(id=Tid)
            message = ChatMessage.objects.filter(thread = thread)
            serilizer = MesageSerializer(message,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        search = request.data.get('search')
        if search == '':
            return Response(status=status.HTTP_404_NOT_FOUND)
        users = User.objects.filter(name__icontains=search)
        serilizer = UserSerializer(users, many=True)
        return Response(serilizer.data)
    
class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            friendId = request.data.get('friendId')
            print(friendId)
            user = request.user
            friend = User.objects.get(id=friendId)
            
            Thread.objects.create(first_person=user,second_person = friend)
            
            
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class RemoveFriendView(APIView):
    def post(self,request):
        try:
            threadId = request.data.get('threadId')
            print(threadId)
            thread = Thread.objects.get(id=threadId)
            thread.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)