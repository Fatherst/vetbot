# Generated by Django 4.2.7 on 2024-01-19 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bonuses", "0007_bonusaccural"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bonusaccural",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="bonusaccural",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
        ),
        migrations.AlterField(
            model_name="bonusaccural",
            name="reason",
            field=models.CharField(
                choices=[
                    ("BIRTHDAY", "День рождения пациента"),
                    ("FIRST_BONUS", "Бонус за регистрацию"),
                    ("REFERAL_SENDER", "Бонус за приглашенного клиента"),
                    ("REFERAL_GETTER", "Бонус за получение приглашения"),
                    ("MANUAL", "Ручное начисление"),
                ],
                max_length=200,
                verbose_name="Причина начисления",
            ),
        ),
    ]
