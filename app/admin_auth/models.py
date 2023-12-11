from django.db import models

from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    tg_chat_id = models.IntegerField(
        null=True, blank=True, verbose_name="Telegram Id", unique=True
    )

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"
