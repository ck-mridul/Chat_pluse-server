from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id','name', 'email', 'image','password','username')
        
    def create(self, validated_data):
        user = User.objects.create(
            name = validated_data['name'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        if 'image' in validated_data:
            instance.image.delete()
            instance.image = validated_data.get('image')
            
        instance.save()
        return instance