from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Element(models.Model):
    name=models.TextField()
    data=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=80, default='non')

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    oz=models.IntegerField(default=0)
    groups=models.ManyToManyField(
        Group,
        related_name='customuserss_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuserd_set',
        blank=True,
    )

    def __str__(self):
        return self.username

from django.contrib.auth.models import User
class User(AbstractUser):
    customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True,
    )

class Ank(models.Model):
    event_name = models.CharField("Название мероприятия", max_length=100)
    user_name = models.CharField("ФИО", max_length=100)
    event_photo = models.ImageField("Фото с ивента", upload_to='event_photos', null=True, blank=True)