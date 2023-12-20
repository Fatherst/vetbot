from django.db import models
from client_auth.models import Client


class DiscountCardCategory(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    name = models.CharField(
        max_length=150, null=True, blank=True, verbose_name="Название"
    )

    class Meta:
        verbose_name = "Категория дисконтных карт"
        verbose_name_plural = "Категории дисконтных карт"


class DiscountCard(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    card_number = models.CharField(
        max_length=150, verbose_name="Номер карты", unique=True
    )
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    category = models.ForeignKey(
        DiscountCardCategory,
        on_delete=models.PROTECT,
        verbose_name="Категория карты",
        blank=True,
        null=True,
    )
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    class Meta:
        verbose_name = "Дисконтная карта"
        verbose_name_plural = "Дисконтные карты"
