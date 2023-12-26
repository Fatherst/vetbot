from django.db import models


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
        max_length=150, verbose_name="Номер карты", blank=True, null=True, unique=False
    )
    client = models.ForeignKey(related_name="discount_cards",
        to="client_auth.Client", on_delete=models.PROTECT, verbose_name="Клиент", blank=True, null=True
    )
    category = models.ForeignKey(
        DiscountCardCategory,
        on_delete=models.SET_NULL,
        verbose_name="Категория карты",
        blank=True,
        null=True,
    )
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    class Meta:
        verbose_name = "Дисконтная карта"
        verbose_name_plural = "Дисконтные карты"


class BonusTransaction(models.Model):
    enote_id = models.CharField(max_length=150, unique=True, db_index=True)
    sum = models.IntegerField()
    discount_card = models.ForeignKey(related_name="bonus_transactions",
                                      to=DiscountCard, on_delete=models.PROTECT)
    transaction_datetime = models.DateTimeField()
