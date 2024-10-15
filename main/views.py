from django.shortcuts import render, redirect
from user_agents import parse

from main.forms import PasswordForm


def home(request):
    return render(request, 'main/home.html')

def mobile_version(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')

    if not user_agent_string:
        # Обработка случая, если User-Agent не найден
        return render(request, 'main/home.html')

    user_agent = parse(user_agent_string)
    is_mobile = user_agent.is_mobile

    if is_mobile:
        return render(request, 'main/mobile_version.html')
    else:
        return render(request, 'main/home.html')

def password_check_view(request):
    next_url = request.GET.get('next')
    session = request.session

    # Проверяем наличие ключа 'attempts' в сессии
    if 'attempts' not in session:
        session['attempts'] = 3

    attempts_left = session['attempts']

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == '52222011':
                session['attempts'] = 3  # Сбрасываем попытки
                return redirect(next_url)
            elif password == '89787676':
                session['attempts'] = 3  # Сбрасываем попытки
                return redirect(next_url)
            elif password == '123451234123121':
                session['attempts'] = 3  # Сбрасываем попытки
                return redirect(next_url)
            else:
                session['attempts'] -= 1
                attempts_left = session['attempts']
                if attempts_left == 0:
                    # Вернем страницу с сатанинскими символами
                    # ...
                    session['attempts'] = 3
                    return render(request, 'main/satanic_error.html')
        else:
            # Ошибка формы
            return render(request, 'main/password_check.html',
                          {'form': form, 'attempts_left': attempts_left, 'next_url': next_url})
    else:
        form = PasswordForm()

    return render(request, 'main/password_check.html', {'form': form, 'attempts_left': attempts_left, 'next_url': next_url})