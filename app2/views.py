from django.shortcuts import render, redirect
from .models import Element, CustomUser
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

def page1(request):
    return render(request, 'app2/page1.html')
def page2(request):
    elem=Element.objects.all().order_by('data')[:10]
    return render(request, 'app2/page2.html', {'elem': elem})


def page3(request):
    top_users = CustomUser.objects.annotate(oz_rank=F('oz')).order_by('-oz_rank')[:20]

    # Проверка авторизации
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.id not in [user.id for user in top_users]:
            top_users = list(top_users)
            top_users.append(current_user.customuser)
            top_users.sort(key=lambda x: x.oz, reverse=True)
    else:
        # Обработка неавторизованных пользователей (например, отображение сообщения)
        return render(request, 'app2/page3.html', {'top_users': top_users, 'message': 'Пожалуйста, войдите в систему.'})

    if current_user.id not in [user.id for user in top_users]:
        top_users = list(top_users)
        top_users.append(current_user.customuser)
        top_users.sort(key=lambda x: x.oz, reverse=True)

    # Создание диаграммы с помощью matplotlib
    fig, ax = plt.subplots() # Удалили лишнюю строку создания fig и ax
    # Цвета из CSS
    coral_color = '#FF7F50'
    blue_color = '#000080'

    # Создание эффекта градиента
    for i, user in enumerate(top_users):
        if i % 2 == 0: # Четные столбцы - darkorange
            ax.bar(user.username, user.oz, color='darkorange', edgecolor='orangered', linewidth=1)
        else: # Нечетные столбцы - orange
            ax.bar(user.username, user.oz, color='orange', edgecolor='orangered', linewidth=1)

    # Дополнительные настройки
    ax.set_xlabel("ОЗ")

    ax.set_facecolor('lightblue') # Синий фон диаграммы

    # Добавление окантовки "outset"
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_edgecolor('darkblue')
        ax.spines[spine].set_linewidth(2)
        ax.spines[spine].set_linestyle('-') # Сплошная линия

    # Убираем пробелы между столбцами
    ax.set_xticks(np.arange(len(top_users)))
    ax.set_xticklabels([user.username for user in top_users], rotation=0, ha='right')

    plt.title("ОЗ пользователей")

    # Изменяем фон изображения
    fig.patch.set_facecolor('lightblue') # Синий фон всего изображения
    fig.patch.set_edgecolor('blue') # Фиолетовая окантовка
    fig.patch.set_linewidth(1)

    # Сохранение диаграммы в объект io.BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=False, dpi=300)
    buf.seek(0)

    # Преобразование изображения в строку base64
    image_data = base64.b64encode(buf.read()).decode('utf-8')

    # Передача данных в шаблон
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
            user=form.save()
            customuser=CustomUser.objects.create(user=user, username=user.username)
            return redirect('logun')  # перенаправление на страницу успеха
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