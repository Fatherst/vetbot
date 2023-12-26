# Generated by Django 4.2.7 on 2023-12-26 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("client_auth", "0006_remove_client_bonuses_balance"),
        ("bonuses", "0003_bonustransaction"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bonustransaction",
            options={
                "verbose_name": "Транзакция по бонусной карте",
                "verbose_name_plural": "Транзакции по бонусной карте",
            },
        ),
        migrations.RenameField(
            model_name="bonustransaction",
            old_name="transaction_datetime",
            new_name="datetime",
        ),
        migrations.AlterField(
            model_name="bonustransaction",
            name="discount_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bonus_transactions",
                to="bonuses.discountcard",
            ),
        ),
        migrations.AlterField(
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
    ]
