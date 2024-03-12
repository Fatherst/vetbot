from django.contrib import admin
from .models import Client, BlockedClient, Patient, AnimalKind, Weighing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone_number",
        "tg_chat_id",
    )
    search_fields = ["enote_id", "last_name", "phone_number"]


@admin.register(BlockedClient)
class BlockedClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reason",
        "created_at",
        "client_id",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "name",
        "birth_date",
        "time_of_death",
        "deleted",
        "kind",
        "client",
    )
    list_display_links = ["name"]
    search_fields = ["enote_id"]


@admin.register(AnimalKind)
class AnimalKindAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "name",
    )
    search_fields = ["enote_id"]


@admin.register(Weighing)
class WeighingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "date",
        "patient",
        "weight",
    )
    list_display_links = ["enote_id"]
    search_fields = ["enote_id"]
