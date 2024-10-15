from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import password_check_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.mobile_version, name='mobile_version'),
    path('app2/', include('app2.urls')),
    path('app1/', include('app1.urls')),
    path('chats/', include('chats.urls')),
    path('password-check/', password_check_view, name='password_check'),
]

urlpatterns += staticfiles_urlpatterns()