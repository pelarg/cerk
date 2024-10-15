from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = 'chats/login.html'
    success_url = 'chats/profile'