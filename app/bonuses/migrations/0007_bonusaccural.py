# Generated by Django 4.2.7 on 2024-01-19 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("client_auth", "0009_weighing"),
        ("bonuses", "0006_alter_program_created_at_alter_program_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BonusAccural",
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
                ("amount", models.PositiveIntegerField(verbose_name="Сумма")),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("BIRTHDAY", "День рождения пациента"),
                            ("REGISTRATION", "Бонус за регистрацию"),
                            ("REFERAL_SENDER", "Бонус за приглашенного клиента"),
                            ("REFERAL_GETTER", "Бонус за получение приглашения"),
                            ("MANUAL", "Ручное начисление"),
                        ],
                        max_length=200,
                        verbose_name="Причина начисления",
                    ),
                ),
                (
                    "accured",
                    models.BooleanField(default=False, verbose_name="Начислено"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bonus_accurals",
                        to="client_auth.client",
                        verbose_name="Клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Начисление бонусов",
                "verbose_name_plural": "Начисления бонусов",
            },
        ),
    ]
