from django.shortcuts import render, redirect
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
            messages.success(request, "Регистрация прошла нормально!")
            UserProfile.objects.create(user=user, nickname=nickname, phone=phone)
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

@login_required(login_url='register2')
def chat_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('register2')
    chats = Chat.objects.filter(users=user_profile)
    return render(request, 'chats/chat_list.html', {'chats': chats})

@login_required(login_url='register2')
def chat_detail(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.method == 'POST':
        if request.user.userprofile.role == 1 and chat.title != 'Чат с админом':
            # Пользователь не может писать в этом чате
            return render(request, 'chats/chat_detail.html', {'chat': chat, 'messages': messages, 'error': 'У вас нет прав для написания в этом чате'})

        content = request.POST.get('content')
        message = Message.objects.create(chat=chat, user=request.user, content=content)

        for user in chat.users.all():
            if user != request.user:
                send_mail(
                    f'Новое сообщение в чате {chat.title}',
                    f'В чате {chat.title} появилось новое сообщение: {message.content}',
                    'from@example.com',
                    [user.email],
                )

        return redirect('chats/chat_detail', chat_id=chat.id)

    return render(request, 'chats/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required(login_url='register2')
def new_chat(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        chat = Chat.objects.create(title=title, image=image)
        chat.users.add(request.user)
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