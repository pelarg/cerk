from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.mobile_version, name='mobile_version')
]

urlpatterns += staticfiles_urlpatterns()