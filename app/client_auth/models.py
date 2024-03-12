from django.db import models
import logging
from model_utils import FieldTracker
from integrations.enote.methods import get_balance
from django.conf import settings

logger = logging.getLogger(__name__)


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

    tracker = FieldTracker()

    @property
    def discount_card(self):
        active_discount_cards = self.discount_cards.filter(deleted=False).filter(
            category__enote_id=settings.CATEGORY_ENOTE_ID
        )
        if active_discount_cards.count() == 1:
            return active_discount_cards.first()
        logger.error(
            f"Возникла ошибка с клиентом {self.first_name} {self.last_name} enote_id:"
            f" {self.enote_id}. Больше одной / нет карт для начисления бонусов "
        )
        return False

    @property
    def balance(self):
        card = self.discount_card
        if not card:
            return None
        balance = get_balance(self.enote_id, card.enote_id)
        return balance

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            last_name_first_name = f"{self.last_name} {self.first_name}"
            if self.middle_name:
                full_name = f"{last_name_first_name} {self.middle_name}"
            else:
                full_name = f"{last_name_first_name}"
            return full_name
        return None

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return f"Клиент {self.pk}"

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

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.pk


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
    kind = models.ForeignKey(
        AnimalKind,
        on_delete=models.PROTECT,
        verbose_name="Вид",
        related_name="patients",
    )
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент", related_name="patients"
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.pk

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
