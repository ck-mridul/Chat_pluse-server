import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Thread,ChatMessage
from .serializers import ThreadSerializer,MesageSerializer
from authentication.models import User
from authentication.serializers import UserSerializer
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

class GetAllPeerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            threads = Thread.objects.by_user(user=request.user).order_by('-updated')
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
    
    def get(self,request):
        search = request.query_params.get('search')
        if search == '':
            return Response(status=status.HTTP_404_NOT_FOUND)
        users = User.objects.filter(name__icontains=search)
        serilizer = UserSerializer(users, many=True)
        return Response(serilizer.data)
    
class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            friendId = request.query_params.get('friendId')
            print(friendId)
            user = request.user
            contact = User.objects.get(id=friendId)
            
            thread = Thread.objects.filter(
                           (Q(first_person=user, second_person=contact) | 
                            Q(first_person=contact, second_person=user)))
            
            if thread:
                if thread[0].hide_by_frst or thread[0].hide_by_second:
                    thread[0].hide_by_frst = False
                    thread[0].hide_by_second = False
                    thread[0].save()
                
                response = {
                        'message':'Thread created',
                        'Tid':thread[0].id,
                        'block_by':thread[0].block_by,
                    }
                return Response(response,status=status.HTTP_200_OK)
            
            
            new_thread = Thread.objects.create(first_person=user,second_person = contact)
            response = {
                'message':'Thread created',
                'Tid':new_thread.id,
                'block_by':new_thread.block_by,
               }
            
            return Response(response,status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            threadId = request.data.get('threadId')
            user = request.user
            
            print(threadId)
            thread = Thread.objects.filter(id=threadId,first_person = user)
            if thread:
                print('first')
                thread[0].hide_by_frst = True
            else:
                thread = Thread.objects.filter(id=threadId,second_person = user)
                if thread:
                    print('second')
                    thread[0].hide_by_second = True
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            thread[0].save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class DeleteChatView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request):
        Id = request.query_params.get('chatId')
        try:
            chat = ChatMessage.objects.get(id=Id)
            chat.delete()
            message = {'message':'chatdeleted'}
            return Response(message,status=status.HTTP_200_OK)
        except:
            message = {'error':'NotFound'}
            return Response(message,status=status.HTTP_404_NOT_FOUND)
        
        
class BlockContactView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            threadId = request.data.get('threadId')
            user = request.user
            block_to = request.data.get('block_to')
            
            print(threadId)
            thread = Thread.objects.get(id=threadId)
            if thread.block_by is not None:
                if thread.block_by != user.id:
                    message = {
                    'error':'You cant Unblock!',
                }
                    return Response(message,status=status.HTTP_403_FORBIDDEN)
                thread.block_by = None
                message = {'message':'unblocked'}
            else:
                thread.block_by = user.id
                message = {
                    'message':'blocked',
                    'block_by': user.id
                }
            thread.save()
            
            channel_layer = get_channel_layer()
            other_user_chat_room = f'user_chatroom_{block_to}'
            
            async_to_sync(channel_layer.group_send)(
                other_user_chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(message)
                }
            )
            
            return Response(message,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)