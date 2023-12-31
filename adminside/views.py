from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import status,generics
from rest_framework.response import Response 
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from authentication.models import User

# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
class BlockUserView(APIView):
    permission_classes = [IsAdminUser]
    
    def patch(self,request):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)