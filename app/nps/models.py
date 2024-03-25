from django.db import models
from client_auth.models import Client


class Rating(models.Model):
    score = models.IntegerField(verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оценки")
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        related_name="ratings",
    )
    appointment_date = models.DateField(verbose_name="Дата приёма")

    def __str__(self):
        return f"Оценка {self.score} от клиента {self.client}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
