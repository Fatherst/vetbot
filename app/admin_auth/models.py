from django.db import models

from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    middle_name = models.CharField(max_length=150, default="", blank=True)
    admin_telegram_id = models.IntegerField(null=True)
