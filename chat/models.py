from django.db import models

from django.contrib.auth.models import User


class Room(models.Model):
    name= models.CharField(max_length=100)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_rooms'
    )

    members = models.ManyToManyField(
        User,
        related_name='chat_rooms',
        blank=True
    )
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    content= models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"