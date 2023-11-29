from django.db import models

from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    code = models.IntegerField(null=True)
    middle_name = models.CharField(max_length=150, default='')
    admin_telegram_id = models.IntegerField(null=True)



