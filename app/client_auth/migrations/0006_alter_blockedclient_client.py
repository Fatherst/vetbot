# Generated by Django 4.2.7 on 2024-01-15 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("client_auth", "0005_alter_blockedclient_client"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blockedclient",
            name="client",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="client_auth.client",
            ),
        ),
    ]
