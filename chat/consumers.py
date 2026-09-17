import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message,Room

from .serializers import MessageSerializer

class ChatConsumer(WebsocketConsumer):

    def connect(self):

        if self.scope["user"].is_anonymous:
            self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        room = Room.objects.get(id=self.room_id)

        if room is None:
            self.close()
            return

        if not room.members.filter(id=self.scope["user"].id).exists():
            self.close()
            return


        self.room_group_name = f"chat_{self.room_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


        messages = Message.objects.filter(room_id=self.room_id)
        serializer = MessageSerializer(messages, many=True)


        self.send(text_data=json.dumps({
            "type": "history",
            "messages": serializer.data
        }))



    def receive(self, text_data):

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                "error": "Invalid JSON."
            }))
            return

        content = data.get("content")

        if not content:
            self.send(text_data=json.dumps({
                "error": "Content is required."
            }))
            return

        if len(content) > 1000:
            self.send(text_data=json.dumps({
                "error": "Message cannot exceed 1000 characters."
            }))
            return


        message = Message.objects.create(
            content=content,
            user=self.scope["user"],
            room_id=self.room_id
            )

        serializer = MessageSerializer(message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": serializer.data,
            }
        )


    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
