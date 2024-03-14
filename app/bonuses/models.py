from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, Q
from client_auth.models import Client
from model_utils import FieldTracker


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

    def __str__(self):
        if self.name:
            return self.name
        return f"Категория {self.pk}"


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
    client = models.ForeignKey(
        related_name="discount_cards",
        to="client_auth.Client",
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        DiscountCardCategory,
        on_delete=models.SET_NULL,
        verbose_name="Категория карты",
        blank=True,
        null=True,
    )
    deleted = models.BooleanField(default=False, verbose_name="Удалена")

    class Meta:
        verbose_name = "Дисконтная карта"
        verbose_name_plural = "Дисконтные карты"

    def __str__(self):
        return f"Дисконтная карта клиента {self.client}"

    def __str__(self):
        return f"Транзакция на карту клиента {self.discount_card.client}"


class Program(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Имя программы")
    description = models.TextField(
        verbose_name="Описание программы",
        help_text="Эта информация будет показана клиентам",
    )
    registration_bonus_amount = models.PositiveIntegerField(
        verbose_name="Бонус за регистрацию"
    )
    new_client_bonus_amount = models.PositiveIntegerField(
        verbose_name="Бонус за нового клиента"
    )
    review_bonus_amount = models.PositiveIntegerField(verbose_name="Бонус за отзыв")
    birthday_bonus_amount = models.PositiveIntegerField(
        verbose_name="Бонус на день рождения"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=False, verbose_name="Активна")

    def retrieve_status(self, money_spent):
        return self.statuses.filter(
            Q(start_amount__lte=money_spent)
            & (Q(end_amount__gte=money_spent) | Q(end_amount__isnull=True))
        ).first()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="Только одна программа может быть активна",
            )
        ]
        verbose_name = "Программа лояльности"
        verbose_name_plural = "Программы лояльности"

    def __str__(self):
        return self.name


class Status(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="statuses",
        verbose_name="Программа",
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название статуса",
        help_text="Эта информация будет показана клиентам",
    )
    cashback_amount = models.PositiveIntegerField(verbose_name="Кэшбек")
    start_amount = models.PositiveIntegerField(
        verbose_name="Начальное значение статуса"
    )
    end_amount = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Конечное значение статуса"
    )

    def clean(self):
        status_without_end = Status.objects.filter(
            program=self.program, end_amount=None
        ).first()
        if status_without_end and self.start_amount >= status_without_end.start_amount:
            raise ValidationError(
                {
                    "start_amount": "Начальное значение статуса не может быть больше или равным "
                    "начальному значению статуса с нулевым конечным значением"
                }
            )
        overlaps = Status.objects.filter(program=self.program, end_amount__isnull=False)
        if self.end_amount:
            overlaps = overlaps.exclude(start_amount__gte=self.end_amount).exclude(
                end_amount__lte=self.start_amount
            )
        else:
            overlaps = overlaps.filter(
                start_amount__lte=self.start_amount, end_amount__gte=self.start_amount
            )
        if overlaps.exists():
            raise ValidationError(
                {
                    "start_amount": "Есть пересечения интервалов значения с другим"
                    " статусом в той же программе"
                }
            )
        if not self.end_amount and status_without_end:
            raise ValidationError(
                {
                    "end_amount": "Пустое конечное значение может быть только один раз в программе"
                }
            )
        if self.end_amount and self.end_amount <= self.start_amount:
            raise ValidationError(
                {"end_amount": "Конечное значение должно быть больше начального"}
            )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["program", "name"],
                name="unique_name_per_program",
            )
        ]
        verbose_name = "Статус программы лояльности"
        verbose_name_plural = "Статусы программы лояльности"

    def __str__(self):
        return self.name


class BonusAccrual(models.Model):
    class ReasonChoices(models.TextChoices):
        BIRTHDAY = (
            "BIRTHDAY",
            "День рождения пациента",
        )
        REGISTRATION = (
            "REGISTRATION",
            "Бонус за регистрацию",
        )
        REFERAL_SENDER = (
            "REFERAL_SENDER",
            "Бонус за приглашенного клиента",
        )
        REFERAL_GETTER = (
            "REFERAL_GETTER",
            "Бонус за получение приглашения",
        )
        MANUAL = (
            "MANUAL",
            "Ручное начисление",
        )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        related_name="bonus_accurals",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    reason = models.CharField(
        choices=ReasonChoices.choices,
        max_length=200,
        verbose_name="Причина начисления",
    )
    accrued = models.BooleanField(default=False, verbose_name="Начислено")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = "Начисление бонусов"
        verbose_name_plural = "Начисления бонусов"

    def __str__(self):
        return f"Начисление клиенту: {self.client}"


class Recommendation(models.Model):
    promocode = models.CharField(verbose_name="Промокод", unique=True)
    issued = models.BooleanField(verbose_name="Выдано", default=False)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Пригласивший клиент"
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"

    def __str__(self):
        return f"Рекомендация с промокодом: {self.promocode}"
