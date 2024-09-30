from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.item_listt, name='item_listt'),
    path('item_detail/', views.item_detail, name='item_detail'),
]
urlpatterns += staticfiles_urlpatterns()