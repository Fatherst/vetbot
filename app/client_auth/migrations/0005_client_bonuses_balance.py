# Generated by Django 4.2.7 on 2023-12-26 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "client_auth",
            "0002_blockedclient_squashed_0004_alter_blockedclient_client_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="bonuses_balance",
            field=models.IntegerField(default=0),
        ),
    ]
