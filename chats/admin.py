from django.contrib import admin
from .models import UserProfile, Chat, Message

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'grade', 'role']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'user', 'content', 'timestamp']