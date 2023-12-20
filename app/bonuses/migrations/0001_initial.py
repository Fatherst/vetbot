# Generated by Django 4.2.7 on 2023-12-20 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("client_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscountCardCategory",
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
                        blank=True, max_length=150, null=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория дисконтных карт",
                "verbose_name_plural": "Категории дисконтных карт",
            },
        ),
        migrations.CreateModel(
            name="DiscountCard",
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
                    "card_number",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Номер карты"
                    ),
                ),
                ("deleted", models.BooleanField(default=False, verbose_name="Удален")),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="bonuses.discountcardcategory",
                        verbose_name="Категория карты",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="client_auth.client",
                        verbose_name="Клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Дисконтная карта",
                "verbose_name_plural": "Дисконтные карты",
            },
        ),
    ]
