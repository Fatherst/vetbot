# Generated by Django 4.2.7 on 2023-12-26 08:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client_auth", "0005_client_bonuses_balance"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="bonuses_balance",
        ),
    ]
