# Generated by Django 5.1.1 on 2024-11-01 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0007_alter_ank_event_name_alter_ank_event_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='title',
            field=models.CharField(default='non', max_length=200),
        ),
    ]
