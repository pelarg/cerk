import os

from django.shortcuts import render, redirect

from app2.models import User
from .models import UserProfile, Chat, Message
from .forms import UserRegistrationForm, AddUserToChatForm, UserProfileForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='register2')
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'chats/profile.html', {'profile': user_profile})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            nickname = request.POST.get('nickname')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            messages.success(request, "Регистрация прошла нормально!")

            # Проверка, существует ли уже профиль, и создание нового профиля
            UserProfile.objects.create(user=user, nickname=nickname, phone=phone, email=email)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'chats/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chats')
        else:
            return render(request, 'chats/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'chats/login.html')

from django.conf import settings

@login_required(login_url='register2')
def chat_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    chats = Chat.objects.filter(users=user_profile)

    # Получаем URL для изображений чатов
    for chat in chats:
        # Создайте путь к изображению с помощью os.path.join
        image_path = os.path.join(settings.MEDIA_ROOT, 'chat_images', chat.image.name) 

        # Добавьте атрибут image_url 
        chat.image_url = image_path # Используйте image_path в качестве URL

        # Вывод URL изображения в консоль (для отладки)
        print(f"chat.image_url: {chat.image_url}") 

    return render(request, 'chats/chat_list.html', {'chats': chats}) 

@login_required(login_url='register2')
def add_user_to_chat(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            try:
                user_profile = user.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)
            chat.users.add(user_profile)
            messages.success(request, f'Пользователь {username} добавлен в чат.')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким именем не найден.')
        return redirect('chat_detail', chat_id=chat_id)
    return render(request, 'chats/add_user_to_chat.html', {'chat': chat})


@login_required(login_url='register2')
def chat_detail(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)
    users_in_chat = chat.users.all()

    if request.method == 'POST':
        # Изменено на использование правильного имени related_name
        if chat.title != 'Чат с админом' and request.user.user_profiles.role == 1:
            # Пользователь не может писать в этом чате
            return render(request, 'chats/chat_detail.html', {
                'chat': chat,
                'messages': messages,
                'error': 'У вас нет прав для написания в этом чате',
                'users_in_chat': users_in_chat
            })

        content = request.POST.get('content')
        message = Message.objects.create(chat=chat, user=request.user, content=content)

        """
        for user in chat.users.all():
            if user != request.user:
                profile = request.user.user_profiles  # Получаем профиль пользователя
                send_mail(
                    f'Новое сообщение в чате {chat.title}',
                    f'В чате {chat.title} появилось новое сообщение: {message.content}',
                    'from@example.com',
                    [profile.email],
                )

        return redirect('chats/chat_detail', chat_id=chat.id)
        """
    return render(request, 'chats/chat_detail.html', {'chat': chat, 'messages': messages})


@login_required(login_url='register2')
def new_chat(request):
       if request.method == 'POST':
           title = request.POST.get('title')
           image = request.FILES.get('image')
           chat = Chat.objects.create(title=title, image=image)

           # Получаем UserProfile пользователя
           try:
               user_profile = UserProfile.objects.get(user=request.user)
           except UserProfile.DoesNotExist:
               # Создаем UserProfile, если он отсутствует
               user_profile = UserProfile.objects.create(user=request.user)

           chat.users.add(user_profile) # Добавляем UserProfile в чат
           return redirect('chat_list')

       return render(request, 'chats/new_chat.html')

@login_required(login_url='register2')
def admin_panel(request):
    if request.user.is_staff:
        user_profiles = UserProfile.objects.all()
        return render(request, 'chats/admin_panel.html', {'user_profiles': user_profiles})
    else:
        return redirect('chats/chat_list')

@login_required(login_url='register2')
def admin_chat_panel(request):
    if request.user.is_staff:
        chats = Chat.objects.all()
        return render(request, 'chats/admin_panel.html', {'chats': chats})
    else:
        return redirect('chats/chat_list')

@login_required(login_url='register2')
def add_user_to_chat(request, chat_id):
    if request.method == 'POST':
        chat = Chat.objects.get(id=chat_id)
        form = AddUserToChatForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            chat.users.add(user)
            return redirect('admin_chat_panel')
    else:
        form = AddUserToChatForm()
    return render(request, 'chats/admin_panel.html', {'form': form})


from django.shortcuts import get_object_or_404


@login_required(login_url='register2')
def edit_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')  # Вернуться на страницу админ-панели после сохранения
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'chats/edit_user.html', {'form': form, 'user_profile': user_profile})

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profiles.save()


