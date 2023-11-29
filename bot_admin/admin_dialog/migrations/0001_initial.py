# Generated by Django 4.2.7 on 2023-11-27 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "clientEnoteId",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("firstName", models.CharField(default="", max_length=100)),
                ("middleName", models.CharField(default="", max_length=100)),
                ("lastName", models.CharField(default="", max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phoneNumber", models.CharField(default="", max_length=10)),
                ("clientTelegramid", models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "doctorEnoteId",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Kind",
            fields=[
                ("kindEnoteId", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="VisitKind",
            fields=[
                ("visitKindId", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "patientEnoteId",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("birthDate", models.DateField()),
                ("weight", models.DecimalField(decimal_places=2, max_digits=5)),
                ("timeOfDeath", models.DateTimeField()),
                ("breedEnoteId", models.IntegerField()),
                ("kindEnoteId", models.IntegerField()),
                ("objectState", models.CharField(choices=[], max_length=100)),
                (
                    "clientEnoteId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.client",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Breed",
            fields=[
                (
                    "breedEnoteId",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=150)),
                (
                    "kindEnoteId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.kind",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
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
                ("appointmentType", models.CharField(max_length=150)),
                ("appointmentStatus", models.CharField(max_length=150)),
                ("appointmentDate", models.DateField()),
                ("startTime", models.TimeField()),
                (
                    "clientEnoteId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.client",
                    ),
                ),
                (
                    "doctorEnoteId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.doctor",
                    ),
                ),
                (
                    "patientEnoteId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.patient",
                    ),
                ),
                (
                    "visitKindId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admin_dialog.visitkind",
                    ),
                ),
            ],
        ),
    ]
