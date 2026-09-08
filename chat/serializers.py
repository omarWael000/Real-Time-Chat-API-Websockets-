from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Room,Message

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields= ['username','password']
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data):
        user= User.objects.create_user(username=validated_data['username'],
        password= validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):

    username= serializers.CharField()
    password= serializers.CharField()

    def validate(self,data):

        user= authenticate(username= data['username'],password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        data['user']=user
        
        return data



class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model= Room
        fields = ['id','name','created_at']
        read_only_fields=['id','created_at']
       




class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Message
        fields=fields = ['id','content','user','room','created_at']
        read_only_fields=['id','created_at','user']
        