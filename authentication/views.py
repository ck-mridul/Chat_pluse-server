from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(APIView):
    def post(self,request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email = email)
        except:
            error = "User Blocked!"
            return Response(error,status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            
            password = request.data.get('password')
            
            if user.check_password(password):
                serializer = UserSerializer(user)
                tokens = get_token(user) 
                
                response = Response()
                response.set_cookie(key='refresh', value=tokens['refresh'], httponly=True, samesite="none", secure=True)
                response.set_cookie(key='access', value=tokens['access'], httponly=True, samesite="none", secure=True)
                
                response.data = {
                    'user': serializer.data, 
                    'tokens': tokens,
                }
                response.status_code = status.HTTP_200_OK
                return response
            error = "Incorrect Password!"
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        error = "User Blocked!"
        return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        
class AdminLoginView(APIView):    
    def post(self,request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email = email)
        except:
            error = "User Blocked!"
            return Response(error,status=status.HTTP_404_NOT_FOUND)
            
        if not user.is_superuser:
            error = "Access denied!"
            return Response(error,status=status.HTTP_401_UNAUTHORIZED)
        
        password = request.data.get('password')
        
        if user.check_password(password):
            serializer = UserSerializer(user)
            tokens = get_token(user) 
            data = {
                'user': serializer.data, 
                'tokens': tokens,
            }
            return Response(data, status=status.HTTP_200_OK)
        error = "Incorrect Password!"
        return Response(error, status=status.HTTP_401_UNAUTHORIZED)
            
        
        
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = request.user
        serializer = self.get_serializer(user,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class EmailVerificationView(APIView):
        
    def post(self,request):
        token = request.data.get('token')
        try:
            user = User.objects.get(token=token)
        except:
            error = 'Invalid token!'
            return Response(error,status=status.HTTP_400_BAD_REQUEST)
        
        if user.token == token and user.is_verified == False:
            user.is_verified =True
            user.save()
            return Response(status=status.HTTP_200_OK)
        
        elif user.is_verified:
            error = 'Email already verified!'
            return Response(error,status=status.HTTP_400_BAD_REQUEST)
        
        
    
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

def get_token(user):
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
class GetUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(request):
        try:
            user = UserSerializer(request.user)
            return Response(user.data)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
            