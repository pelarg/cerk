from django.shortcuts import render
from user_agents import parse

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