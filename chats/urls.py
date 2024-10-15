from django.urls import path
from .views import register, profile, chat_list, chat_detail, new_chat, admin_panel, edit_user
from .logio import CustomLoginView
from django.contrib.auth.views import LoginView
from .views import admin_chat_panel
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('register2/', register, name='register2'),
    path('profile/', profile, name='profile'),
    path('chats/', chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chat/new/', new_chat, name='new_chat'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('admin/chats/', admin_chat_panel, name='admin_chat_panel'),
    path('admin/edit_user/<int:user_id>/', edit_user, name='edit_user'),
]

urlpatterns += staticfiles_urlpatterns()