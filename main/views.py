from django.shortcuts import render
from user_agents import parse

def home(request):
    return render(request, 'main/home.html', {})

def mobile_version(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    is_mobile = user_agent.is_mobile

    if is_mobile:
        return render(request, 'main/mobile_version.html')
    else:
        return render(request, 'main/home.html')