# Generated by Django 4.2.7 on 2023-11-27 08:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_dialog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="phoneNumber",
            field=models.CharField(default="", max_length=12),
        ),
    ]
