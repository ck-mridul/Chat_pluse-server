import uuid
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .send_mails import send_verification_email


class WelcomeView(APIView):
    def get(self):
        return Response({'message':'Welcome'})

class UserRegisterView(APIView):

    def post(self,request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user:
            return Response('Email already Exist!',status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            user_obj = User.objects.get(email=email)
            uid = str(uuid.uuid4())
            user_obj.token = uid
            user_obj.save()
            print(email,'email')
            # change celery to normal due to hosting on rendor
            send_verification_email(email,uid)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response('Somthig Error!',status=status.HTTP_400_BAD_REQUEST)
        
        
class UserLoginView(APIView):
    def post(self,request):
        try:
            try:
                email = request.data.get('email')
                user = User.objects.get(email = email)
            except:
                error = "User not found!"
                return Response(error,status=status.HTTP_404_NOT_FOUND)
            
            if not user.is_active:
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
            error = "User not Verified!"
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        except:
            error = "Something is wrong!"
            return response(error, status=status.HTTP_400_BAD_REQUEST)

        
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = request.user
        username = request.data.get('username')
        if username:
            user_obj = User.objects.filter(username = username).exclude(id=user.id)
            if user_obj:
                erro_message = {'error':'username already exist!'}
                
                return Response(erro_message,status=status.HTTP_406_NOT_ACCEPTABLE)
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
        
     

def get_token(user):
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        


            