from django.db import models
from client_auth.models import Client
from admin_auth.models import Admin


class Dialogue(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    topic_choices = []
    topic = models.CharField(max_length=250, choices=topic_choices)
    operator = models.ForeignKey(Admin, on_delete=models.PROTECT)
    state_choices = []
    state = models.CharField(max_length=150, choices=state_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()


class Message(models.Model):
    """
    Зачем дублировать телеграммовский объект сообщения?
    Связать с телеграммовским объектом?
    Время есть, телеграм айди есть, есть айди, равное количеству сообщений, присланных в этом чате
    """

    id = models.IntegerField(primary_key=True)
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE)
