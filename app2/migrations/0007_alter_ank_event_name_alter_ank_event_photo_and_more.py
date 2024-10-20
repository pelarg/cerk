# Generated by Django 5.1.1 on 2024-10-12 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0006_ank_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ank',
            name='event_name',
            field=models.CharField(max_length=100, verbose_name='Название мероприятия'),
        ),
        migrations.AlterField(
            model_name='ank',
            name='event_photo',
            field=models.ImageField(blank=True, null=True, upload_to='event_photos', verbose_name='Фото с ивента'),
        ),
        migrations.AlterField(
            model_name='ank',
            name='user_name',
            field=models.CharField(max_length=100, verbose_name='ФИО'),
        ),
    ]
