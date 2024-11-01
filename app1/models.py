from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    is_used = models.BooleanField(default=False) # Добавляем поле "is_used"

    def __str__(self):
        return self.title