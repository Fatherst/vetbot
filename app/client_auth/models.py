from bot.bot_init import logger
from django.conf import settings
from django.db import models
from integrations.enote.methods import ClientBalance, get_balance
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

    tracker = FieldTracker()

    @property
    def discount_card(self):
        discount_cards = self.discount_cards.filter(
            deleted=False, category__enote_id=settings.CATEGORY_ENOTE_ID
        )
        if discount_cards.count() == 1:
            return discount_cards.first()
        logger.error(
            f"Возникла ошибка с клиентом {self.id}: Больше одной/нет карт "
            "для начисления бонусов"
        )
        return False

    @property
    def balance(self) -> ClientBalance:
        if self.discount_card:
            return get_balance(self.enote_id, self.discount_card.enote_id)
        return ClientBalance(money_spent=0, bonus_balance=0)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            full_name = f"{self.last_name} {self.first_name}"
            full_name += f" {self.middle_name}" if self.middle_name else ""
            return full_name
        return None

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return f"Клиент {self.pk}"

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
<<<<<<< HEAD
            return f"Вид животного {self.pk}"
=======
            return self.pk
>>>>>>> webhooks


class BlockedClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    reason = models.TextField(blank=True, null=True, verbose_name="Причина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заблокированный клиент"
        verbose_name_plural = "Заблокированные клиенты"

    def __str__(self):
        return self.client


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
    deleted = models.BooleanField(default=False, verbose_name="Удалён")
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
<<<<<<< HEAD
            return f"Пациент {self.pk}"
=======
            return self.pk
>>>>>>> webhooks

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

    def __str__(self):
        return f"Взвешивание пациента {self.patient}"
