from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tg_chat_id = models.IntegerField(verbose_name="Telegram Id", unique=True)

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"
