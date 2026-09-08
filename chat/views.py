from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer,LoginSerializer,RoomSerializer

from .models import Room

class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):

        if id is None:
            rooms= Room.objects.all()
            serializer = RoomSerializer(rooms,many=True)
            return Response(serializer.data)

        room= get_object_or_404(Room,id=id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
        



    def post(self,request):

        serializer=RoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    



class RegisterView(APIView):

    def post(self,request):

        serializer= RegisterSerializer(data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"},
            status=status.HTTP_201_CREATED)

        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self,request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token,created = Token.objects.get_or_create(user=user) 

            return Response({'token':token.key})

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)