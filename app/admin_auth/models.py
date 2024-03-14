from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь"
    )
    tg_chat_id = models.IntegerField(verbose_name="Telegram Id", unique=True)

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return str(self.user)
