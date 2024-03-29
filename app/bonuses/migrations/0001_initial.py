# Generated by Django 4.2.7 on 2024-03-15 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("client_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BonusAccrual",
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
                    "accrued",
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
            ],
            options={
                "verbose_name": "Начисление бонусов",
                "verbose_name_plural": "Начисления бонусов",
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
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Номер карты",
                    ),
                ),
                ("deleted", models.BooleanField(default=False, verbose_name="Удалена")),
            ],
            options={
                "verbose_name": "Дисконтная карта",
                "verbose_name_plural": "Дисконтные карты",
            },
        ),
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
            name="Program",
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
                    "name",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Имя программы"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Эта информация будет показана клиентам",
                        verbose_name="Описание программы",
                    ),
                ),
                (
                    "registration_bonus_amount",
                    models.PositiveIntegerField(verbose_name="Бонус за регистрацию"),
                ),
                (
                    "new_client_bonus_amount",
                    models.PositiveIntegerField(verbose_name="Бонус за нового клиента"),
                ),
                (
                    "review_bonus_amount",
                    models.PositiveIntegerField(verbose_name="Бонус за отзыв"),
                ),
                (
                    "birthday_bonus_amount",
                    models.PositiveIntegerField(verbose_name="Бонус на день рождения"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="Активна"),
                ),
            ],
            options={
                "verbose_name": "Программа лояльности",
                "verbose_name_plural": "Программы лояльности",
            },
        ),
        migrations.CreateModel(
            name="Status",
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
                    "name",
                    models.CharField(
                        help_text="Эта информация будет показана клиентам",
                        max_length=150,
                        verbose_name="Название статуса",
                    ),
                ),
                ("cashback_amount", models.PositiveIntegerField(verbose_name="Кэшбек")),
                (
                    "start_amount",
                    models.PositiveIntegerField(
                        verbose_name="Начальное значение статуса"
                    ),
                ),
                (
                    "end_amount",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Конечное значение статуса"
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="statuses",
                        to="bonuses.program",
                        verbose_name="Программа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статус программы лояльности",
                "verbose_name_plural": "Статусы программы лояльности",
            },
        ),
        migrations.CreateModel(
            name="Recommendation",
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
                ("promocode", models.CharField(unique=True, verbose_name="Промокод")),
                ("issued", models.BooleanField(default=False, verbose_name="Выдано")),
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
                        to="client_auth.client",
                        verbose_name="Пригласивший клиент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рекомендация",
                "verbose_name_plural": "Рекомендации",
            },
        ),
        migrations.AddConstraint(
            model_name="program",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("is_active",),
                name="Только одна программа может быть активна",
            ),
        ),
        migrations.AddField(
            model_name="discountcard",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="bonuses.discountcardcategory",
                verbose_name="Категория карты",
            ),
        ),
        migrations.AddField(
            model_name="discountcard",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="discount_cards",
                to="client_auth.client",
                verbose_name="Клиент",
            ),
        ),
        migrations.AddField(
            model_name="bonusaccrual",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bonus_accurals",
                to="client_auth.client",
                verbose_name="Клиент",
            ),
        ),
        migrations.AddConstraint(
            model_name="status",
            constraint=models.UniqueConstraint(
                fields=("program", "name"), name="unique_name_per_program"
            ),
        ),
    ]
