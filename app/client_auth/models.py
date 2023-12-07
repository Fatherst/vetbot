from django.db import models


class Client(models.Model):
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    enote_id = models.CharField(max_length=150)
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    middle_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    phone_number = models.CharField(max_length=12, default="")
    tg_chat_id = models.IntegerField(null=True, default=0)
