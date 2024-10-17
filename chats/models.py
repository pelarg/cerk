from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Изменено на ForeignKey
    nickname = models.CharField(max_length=30)
    grade = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    role = models.IntegerField(default=1)

    def __str__(self):
        return self.nickname


class Chat(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chat_images/')
    users = models.ManyToManyField(UserProfile, related_name='chats')

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in {self.chat.title}: {self.content}'