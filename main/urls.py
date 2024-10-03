from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.mobile_version, name='mobile_version'),
    path('app2/', include('app2.urls')),
    path('app1/', include('app1.urls'))
]

urlpatterns += staticfiles_urlpatterns()