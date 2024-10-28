from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('item_lisst/', views.item_lisst, name='item_lisst'),
    path('register/', views.register, name='register'),
    path('anketa/', views.anketa, name='anketa'),
    path('download/', views.download_file, name='download_file'),
]
urlpatterns += staticfiles_urlpatterns()