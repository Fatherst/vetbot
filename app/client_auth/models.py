from django.db import models
from django.db.models import Sum
from asgiref.sync import sync_to_async
from model_utils import FieldTracker


class Client(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Имя"
    )
    middle_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Отчество"
    )
    last_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Фамилия"
    )
    email = models.EmailField(verbose_name="E-mail", null=True, blank=True)
    phone_number = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="Телефон", unique=False
    )
    tg_chat_id = models.IntegerField(
        null=True, blank=True, verbose_name="Telegram Id", unique=True
    )
    deleted = models.BooleanField(default=False, verbose_name="Удалён")

    @property
    async def balance(self):
        card = await self.discount_cards.afirst()
        if not card:
            return 0
        balance = await sync_to_async(
            lambda: card.bonus_transactions.aggregate(total_balance=Sum("sum"))[
                "total_balance"
            ]
        )()
        return balance

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class AnimalKind(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Название"
    )

    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды"


class BlockedClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заблокированный клиент"
        verbose_name_plural = "Заблокированные клиенты"


class Patient(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    time_of_death = models.DateTimeField(
        null=True, blank=True, verbose_name="Время смерти"
    )
    deleted = models.BooleanField(default=False, verbose_name="Пометить на удаление")
    kind = models.ForeignKey(AnimalKind, on_delete=models.PROTECT, verbose_name="Вид")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


class Weighing(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        verbose_name="Пациент",
        related_name="weighings",
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вес")
    date = models.DateTimeField(null=True, blank=True, verbose_name="Дата взвешивания")

    class Meta:
        verbose_name = "Взвешивание"
        verbose_name_plural = "Взвешивания"
