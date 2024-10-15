from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    grade = models.CharField(max_length=10)  # Класс
    phone = models.CharField(max_length=15)
    role = models.IntegerField(default=1)  # 1 = обычный пользователь, 2 = модератор, 3 = админ

    def __str__(self):
        return self.nickname

class Chat(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chat_images/')
    users = models.ManyToManyField(UserProfile, related_name='chats')  # Изменено на UserProfile

    def __str__(self):
        return self.title

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in {self.chat.title}: {self.content}'