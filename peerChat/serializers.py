from rest_framework import serializers
from .models import Thread,ChatMessage
from authentication.serializers import UserSerializer

class ThreadSerializer(serializers.ModelSerializer):
    first_person = UserSerializer()
    second_person = UserSerializer()
    
    class Meta:
        model = Thread
        fields = '__all__'
        depth = 1
        
class MesageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatMessage
        fields = '__all__'

