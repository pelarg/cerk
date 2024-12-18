import os

import matplotlib
from django.shortcuts import render, redirect

from .models import Element, CustomUser, User
from .forms import RegistrationForm
from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.pyplot import figure
matplotlib.use('Agg')

def page1(request):
    return render(request, 'app2/page1.html')
def page2(request):
    elem=Element.objects.all().order_by('data')[:10]
    return render(request, 'app2/page2.html', {'elem': elem})

def page3(request):
    # Получить 20 пользователей с максимальным значением oz
    top_users = CustomUser.objects.annotate(oz_rank=F('oz')).order_by('-oz_rank')[:20]

    # Проверка наличия пользователей
    if not top_users:
        print("Нет пользователей для отображения.")
        return render(request, 'app2/page3.html', {'message': 'Нет пользователей для отображения.'})

    # Переписываем текущего пользователя
    try:
        current_user = CustomUser.objects.get(username=request.user.username)  # Получаем объект CustomUser
    except CustomUser.DoesNotExist:
        return render(request, 'app2/page3.html', {'top_users': top_users, 'message': 'Текущий пользователь не найден.'})

    if current_user not in top_users:
        top_users = list(top_users)  # Преобразуем QuerySet в список
        top_users.append(current_user)  # Добавляем текущего пользователя
        top_users = sorted(top_users, key=lambda x: x.oz, reverse=True)  # Сортировка по полю oz

    # Создание диаграммы
    fig, ax = plt.subplots(figsize=(12, 6))  # Установка фиксированной ширины и высоты

    # Создание столбчатой диаграммы
    for i, user in enumerate(top_users):
        color = 'darkorange' if i % 2 == 0 else 'orange'
        ax.bar(user.username, user.oz, color=color, edgecolor='orangered', linewidth=1)

    ax.set_xlabel("Пользователи", fontsize=14)
    ax.set_ylabel("ОЗ", fontsize=14)
    ax.set_title("ОЗ пользователей", fontsize=16)
    ax.set_facecolor('lightblue')

    # Настройка меток оси X
    ax.set_xticks(np.arange(len(top_users)))
    ax.set_xticklabels([user.username for user in top_users], rotation=0, ha='right', fontsize=10)

    # Сохранение диаграммы
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)

    buf.seek(0)
    image_data = base64.b64encode(buf.read()).decode('utf-8')

    if not image_data:
        print("Не удалось закодировать изображение.")
        return render(request, 'app2/page3.html', {'message': 'Не удалось сгенерировать диаграмму.'})

    context = {
        "top_users": top_users,
        "image_data": image_data,
        "current_user": current_user,
    }
    return render(request, 'app2/page3.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Сначала сохранить пользователя
            user = form.save(commit=False)
            user.save()
            # Создание связанного объекта User
            user_instance = User.objects.create(username=user.username, password=user.password)
            # Создайте связь с CustomUser
            user_instance.customuser = user  # Установите связь
            user_instance.save()  # Сохраните объект User
            return redirect('page1')  # Здесь должна быть ваша страница успешной регистрации
    else:
        form = RegistrationForm()

    return render(request, 'app2/register.html', {'form': form})

def success_view(request):
    pass

def item_lisst(request):
    return render(request, 'app2/item_lisst.html')

def login_view(request):
    return render(request, 'app2/page1.html')
from django.shortcuts import render, redirect
from .forms import AnkForm
from .models import Ank

def anketa(request):
    if request.method == 'POST':
        form = AnkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('page2')
    else:
        form = AnkForm()
    return render(request, 'app2/anketa.html', {'form': form})

import os
from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.conf import settings

def download_file(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'app2', '00', '00.docx')

    if not os.path.exists(file_path):
        return HttpResponse("Файл не найден", status=404)

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="your_file.pdf"'
    return response