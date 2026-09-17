from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer,LoginSerializer,RoomSerializer,MessageSerializer,AddMemberSerializer

from .models import Room,Message

from django.contrib.auth.models import User

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
            room = serializer.save(owner=request.user)
            room.members.add(request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        



class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):

        if id is None:
            messages = Message.objects.all()

        else:
            room = get_object_or_404(Room, id=id)

            if not room.members.filter(id=request.user.id).exists():
                return Response(
                {"detail": "You are not a member of this room."},
                status=status.HTTP_403_FORBIDDEN
            )

            messages = Message.objects.filter(room=room)


        serializer= MessageSerializer(messages,many=True)
        return Response(serializer.data)



    def post(self,request):

        serializer= MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
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

        
class RoomMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,id):

        room=get_object_or_404(Room,id=id)

        if room.owner != request.user:
            return Response(
                {"detail": "Only the room owner can add members."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer= AddMemberSerializer(data=request.data)

        if serializer.is_valid():
            user= get_object_or_404(User,id=serializer.validated_data['user_id'])
            room.members.add(user)

            return Response(
                {"detail": "User added to room."},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
