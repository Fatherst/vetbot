from django.db import models
from client_auth.models import Client
from model_utils import FieldTracker


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


class Review(models.Model):
    class StatusChoices(models.TextChoices):
        UNCHECKED = (
            "UNCHECKED",
            "Не проверено",
        )
        APPROVED = (
            "APPROVED",
            "Скриншот проверен",
        )
        REJECTED = (
            "REJECTED",
            "Скриншот отклонён",
        )

    class ResourceChoices(models.TextChoices):
        GOOGLE = (
            "GOOGLE",
            "Google",
        )
        YANDEX = (
            "YANDEX",
            "Yandex",
        )

    screenshot = models.FileField(
        upload_to="review_screenshots/", verbose_name="Скриншот"
    )
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент", related_name="reviews"
    )
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.UNCHECKED,
        verbose_name="Статус проверки",
    )
    resource = models.CharField(
        max_length=50, verbose_name="Источник отзыва", choices=ResourceChoices.choices
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    modified_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    tracker = FieldTracker()

    def __str__(self):
        return f"Отзыв в {self.resource} от клиента {self.client}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
