# Generated by Django 4.2.7 on 2023-12-18 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnimalKind",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enote_id",
                    models.CharField(
                        db_index=True,
                        max_length=150,
                        unique=True,
                        verbose_name="ID в еноте",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вид",
                "verbose_name_plural": "Виды",
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enote_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="ID в еноте",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Отчество"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Фамилия"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="E-mail"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True, max_length=12, null=True, verbose_name="Телефон"
                    ),
                ),
                (
                    "tg_chat_id",
                    models.IntegerField(
                        blank=True, null=True, unique=True, verbose_name="Telegram Id"
                    ),
                ),
                ("deleted", models.BooleanField(default=False, verbose_name="Удалён")),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enote_id",
                    models.CharField(
                        db_index=True,
                        max_length=150,
                        unique=True,
                        verbose_name="ID в еноте",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата рождения"
                    ),
                ),
                (
                    "time_of_death",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время смерти"
                    ),
                ),
                (
                    "weight",
                    models.FloatField(blank=True, null=True, verbose_name="Вес"),
                ),
                (
                    "deleted",
                    models.BooleanField(
                        default=False, verbose_name="Пометить на удаление"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="client_auth.client",
                        verbose_name="Клиент",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="client_auth.animalkind",
                        verbose_name="Вид",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пациент",
                "verbose_name_plural": "Пациенты",
            },
        ),
    ]
