from django.db import models
from client_auth.models import Patient, Client


class Specialization(models.Model):
    enote_id = models.CharField(
        max_length=150,
        verbose_name="ID в еноте",
        db_index=True,
        unique=True,
    )
    name = models.CharField(max_length=100, verbose_name="Название специализации")

    class Meta:
        verbose_name = "Врачебная специализация"
        verbose_name_plural = "Врачебные специализации"


class Doctor(models.Model):
    enote_id = models.CharField(
        max_length=150, verbose_name="ID в еноте", db_index=True, unique=True
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Отчество"
    )
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    specializations = models.ManyToManyField(
        Specialization,
        related_name="doctors",
        verbose_name="Специализация",
        blank=True,
    )
    photo = models.ImageField(upload_to="doctors/", null=True, blank=True)
    detail_info = models.TextField(blank=True, null=True, verbose_name="Описание врача")
    fired_date = models.DateField(null=True, blank=True, verbose_name="Дата увольнения")
    deleted = models.BooleanField(default=False, verbose_name="Пометить на удаление")

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"


class Appointment(models.Model):
    class StatusChoices(models.TextChoices):
        BOOKING = (
            "BOOKING",
            "Бронирование",
        )
        PLANNED = (
            "PLANNED",
            "Запланировано",
        )
        IN_CLINIC = (
            "IN_CLINIC",
            "В клинике",
        )
        CLINIC_APPOINTMENT = (
            "CLINIC_APPOINTMENT",
            "На приеме",
        )
        REGISTRATION = (
            "REGISTRATION",
            "Оформление",
        )
        COMPLETED = (
            "COMPLETED",
            "Завершено",
        )
        CLIENTS_REFUSAL = (
            "CLIENTS_REFUSAL",
            "Отказ",
        )
        IN_INPATIENTS = (
            "IN_INPATIENTS",
            "Стационар",
        )
        DISCHARGED = (
            "DISCHARGED",
            "Выписан из стационара",
        )

    enote_id = models.CharField(
        max_length=150, verbose_name="ID в еноте", db_index=True, unique=True
    )
    status = models.CharField(
        verbose_name="Статус записи",
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, verbose_name="Пациент", null=True, blank=True
    )
    client = models.ForeignKey(
        Client, default=None, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, verbose_name="Доктор")
    date_time = models.DateTimeField(verbose_name="Время записи")
    deleted = models.BooleanField(default=False, verbose_name="Пометить на удаление")

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"
